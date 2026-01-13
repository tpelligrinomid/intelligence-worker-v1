from app.ai_client import get_completion
from app.firecrawl import scrape_url
from app.models import CompetitorAnalysisInput


SYSTEM_PROMPT = """You are a competitive intelligence analyst helping a B2B marketing team understand a competitor. Your goal is to provide actionable insights that help the client win against this competitor.

Write in a clear, direct style. Be specific with examples from the website. Don't hedge or be vague.

Structure your analysis with these sections:

## Competitor Snapshot
What does this competitor do? (2-3 sentences max)

## Their Business Model
- How do they make money?
- Pricing model (if visible): subscription, per-seat, usage-based, etc.
- Any pricing tiers or packages mentioned?

## What They're Selling
Their main products/services. Note their flagship offering vs. secondary products.

## Who They're Targeting
- Their ideal customer profile
- Industries/verticals they focus on
- Company sizes they seem to target (SMB, mid-market, enterprise)

## Their Positioning & Messaging
- What's their main value proposition?
- Key claims they make
- Messaging themes they emphasize

## Strengths (What They Do Well)
Based on their website, what appears to be their competitive advantages? Be specific.

## Weaknesses & Vulnerabilities
Where do they appear weak? What's missing from their website? Where could our client potentially beat them?

## How to Compete Against Them
Specific recommendations for how our client can differentiate or win against this competitor:
- Messaging angles to emphasize
- Weaknesses to exploit
- Audiences they may be underserving

Keep the total response under 700 words. Focus on actionable competitive intelligence."""


def process(input_data: dict) -> dict:
    parsed = CompetitorAnalysisInput(**input_data)

    url = f"https://{parsed.domain}"
    scraped = scrape_url(url)

    website_content = scraped.get("data", {}).get("markdown", "")
    if not website_content:
        website_content = scraped.get("data", {}).get("content", "No content available")

    prompt = f"""Analyze this competitor:

COMPETITOR: {parsed.company_name}
WEBSITE: {parsed.domain}

OUR CLIENT'S CONTEXT:
{parsed.client_context}

COMPETITOR'S WEBSITE CONTENT:
{website_content[:15000]}

Provide competitive intelligence that helps our client compete against this company. Be specific and actionable."""

    analysis = get_completion(prompt, SYSTEM_PROMPT, provider=parsed.provider)

    return {
        "competitor_name": parsed.company_name,
        "competitor_domain": parsed.domain,
        "analysis": analysis,
        "scraped_content": website_content[:5000],  # Include for downstream use
        "provider_used": parsed.provider,
    }
