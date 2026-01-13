import os
import re
import httpx


FIRECRAWL_API_URL = "https://api.firecrawl.dev/v0"

# Browser-like headers for direct scraping fallback
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


def _html_to_text(html: str) -> str:
    """Basic HTML to text conversion - strips tags and cleans up whitespace."""
    # Remove script and style elements entirely
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<noscript[^>]*>.*?</noscript>", "", html, flags=re.DOTALL | re.IGNORECASE)

    # Remove HTML comments
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    # Replace common block elements with newlines
    html = re.sub(r"</(p|div|h[1-6]|li|tr|br|hr)[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<(br|hr)[^>]*>", "\n", html, flags=re.IGNORECASE)

    # Remove all remaining HTML tags
    html = re.sub(r"<[^>]+>", " ", html)

    # Decode common HTML entities
    html = html.replace("&nbsp;", " ")
    html = html.replace("&amp;", "&")
    html = html.replace("&lt;", "<")
    html = html.replace("&gt;", ">")
    html = html.replace("&quot;", '"')
    html = html.replace("&#39;", "'")

    # Clean up whitespace
    html = re.sub(r"[ \t]+", " ", html)  # Multiple spaces/tabs to single space
    html = re.sub(r"\n\s*\n", "\n\n", html)  # Multiple newlines to double newline
    html = html.strip()

    return html


def _direct_scrape(url: str) -> dict:
    """Fallback: Direct HTTP request to get page content."""
    print(f"Firecrawl failed, attempting direct scrape of {url}")

    response = httpx.get(
        url,
        headers=BROWSER_HEADERS,
        timeout=30.0,
        follow_redirects=True,
    )
    response.raise_for_status()

    html = response.text
    text_content = _html_to_text(html)

    # Return in same format as Firecrawl for compatibility
    return {
        "success": True,
        "data": {
            "markdown": text_content,
            "content": text_content,
        },
        "source": "direct_scrape",
    }


def scrape_url(url: str) -> dict:
    """Scrape URL using Firecrawl, with direct HTTP fallback on failure."""
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    firecrawl_error = None

    # Try Firecrawl first if API key is available
    if api_key:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            response = httpx.post(
                f"{FIRECRAWL_API_URL}/scrape",
                headers=headers,
                json={"url": url},
                timeout=60.0,
            )
            response.raise_for_status()
            result = response.json()
            result["source"] = "firecrawl"
            return result
        except Exception as e:
            firecrawl_error = f"{type(e).__name__}: {e}"
            print(f"Firecrawl error for {url}: {firecrawl_error}")
            # Fall through to direct scrape

    # Fallback to direct scraping
    try:
        return _direct_scrape(url)
    except Exception as e:
        direct_error = f"{type(e).__name__}: {e}"
        print(f"Direct scrape error for {url}: {direct_error}")

        # Both methods failed - return graceful error response
        error_msg = f"Could not access website. Firecrawl: {firecrawl_error or 'skipped'}. Direct: {direct_error}"
        return {
            "success": False,
            "data": {
                "markdown": f"[Website unavailable: {url}]\n\nUnable to scrape this website. The site may be down, blocking automated access, or the domain may not exist.",
                "content": f"Website unavailable: {url}",
            },
            "source": "error",
            "error": error_msg,
        }


def crawl_website(url: str, max_pages: int = 10) -> dict:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY must be set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = httpx.post(
        f"{FIRECRAWL_API_URL}/crawl",
        headers=headers,
        json={
            "url": url,
            "crawlerOptions": {"limit": max_pages},
            "pageOptions": {"onlyMainContent": True},
        },
        timeout=120.0,
    )
    response.raise_for_status()
    return response.json()
