from app.ai_client import get_completion
from app.firecrawl import scrape_url
from app.models import CompanyResearchInput


SYSTEM_PROMPT = """You are an expert business analyst preparing research for a B2B marketing engagement. Your task is to analyze a company and provide insights that will help a marketing team understand who they're working with.

Write in a clear, direct style. Avoid jargon. Be specific with examples from the website content when possible.

Structure your analysis with these sections:

## Company Overview
Brief description of what the company does (2-3 sentences max).

## How They Make Money
This is critical - explain the business model in simple terms:
- What do they sell? (products, services, subscriptions, licenses, etc.)
- Who pays them? (end users, enterprises, advertisers, etc.)
- How are they priced? (subscription tiers, per-seat, usage-based, project-based, etc.)
- What's their primary revenue stream vs. secondary?

## Products & Services
List their main offerings with brief descriptions. Note which seem to be their flagship/core vs. add-ons.

## Target Market
- Who are their ideal customers? (company size, industry, role)
- What problems do they solve for these customers?
- Any specific verticals or niches they focus on?

## Value Proposition
What's their main pitch? Why would someone choose them over alternatives?

## Key Differentiators
What makes them unique or different from competitors? Be specific.

## Red Flags & Gaps
Note anything that seems unclear, missing, or potentially problematic from their website (e.g., no pricing, vague descriptions, outdated content).

Keep the total response under 800 words. Focus on what a marketing team needs to know."""


def process(input_data: dict) -> dict:
    parsed = CompanyResearchInput(**input_data)

    url = f"https://{parsed.domain}"
    scraped = scrape_url(url)

    website_content = scraped.get("data", {}).get("markdown", "")
    if not website_content:
        website_content = scraped.get("data", {}).get("content", "No content available")

    prompt = f"""Analyze this company based on their website content:

COMPANY: {parsed.company_name}
WEBSITE: {parsed.domain}

WEBSITE CONTENT:
{website_content[:15000]}

Provide your analysis following the structure in your instructions. Be specific and use examples from the website content."""

    analysis = get_completion(prompt, SYSTEM_PROMPT, provider=parsed.provider)

    return {
        "company_name": parsed.company_name,
        "domain": parsed.domain,
        "analysis": analysis,
        "scraped_content": website_content[:8000],  # Include for downstream use
        "provider_used": parsed.provider,
    }
