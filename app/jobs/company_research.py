from app.ai_client import get_completion
from app.firecrawl import scrape_url
from app.models import CompanyResearchInput


SYSTEM_PROMPT = """You are an expert business analyst. Your task is to analyze company information and provide comprehensive research insights.

Provide your analysis in a structured format covering:
1. Company Overview
2. Products/Services
3. Target Market
4. Value Proposition
5. Business Model
6. Key Differentiators
7. Notable Information

Be thorough but concise. Focus on actionable insights."""


def process(input_data: dict) -> dict:
    parsed = CompanyResearchInput(**input_data)

    url = f"https://{parsed.domain}"
    scraped = scrape_url(url)

    website_content = scraped.get("data", {}).get("markdown", "")
    if not website_content:
        website_content = scraped.get("data", {}).get("content", "No content available")

    prompt = f"""Analyze the following company:

Company Name: {parsed.company_name}
Website: {parsed.domain}

Website Content:
{website_content[:15000]}

Provide a comprehensive company research report based on the information above."""

    analysis = get_completion(prompt, SYSTEM_PROMPT, provider=parsed.provider)

    return {
        "company_name": parsed.company_name,
        "domain": parsed.domain,
        "analysis": analysis,
        "provider_used": parsed.provider,
    }
