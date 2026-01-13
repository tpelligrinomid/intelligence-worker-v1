import os
import httpx


FIRECRAWL_API_URL = "https://api.firecrawl.dev/v0"


def scrape_url(url: str) -> dict:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY must be set")

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
    return response.json()


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
