from app.ai_client import get_completion
from app.firecrawl import scrape_url
from app.models import CompetitorAnalysisInput


SYSTEM_PROMPT = """You are an expert competitive intelligence analyst. Your task is to analyze a competitor company and provide strategic insights for your client.

Provide your analysis in a structured format covering:
1. Competitor Overview
2. Product/Service Comparison Points
3. Pricing Strategy (if available)
4. Market Positioning
5. Strengths (from client's perspective)
6. Weaknesses/Vulnerabilities
7. Competitive Threats
8. Opportunities for Differentiation
9. Strategic Recommendations

Be thorough and provide actionable competitive intelligence."""


def process(input_data: dict) -> dict:
    parsed = CompetitorAnalysisInput(**input_data)

    url = f"https://{parsed.domain}"
    scraped = scrape_url(url)

    website_content = scraped.get("data", {}).get("markdown", "")
    if not website_content:
        website_content = scraped.get("data", {}).get("content", "No content available")

    prompt = f"""Analyze the following competitor for our client:

Competitor Company: {parsed.company_name}
Competitor Website: {parsed.domain}

Client Context:
{parsed.client_context}

Competitor Website Content:
{website_content[:15000]}

Provide a comprehensive competitive analysis from our client's perspective. Focus on actionable insights that will help our client compete more effectively."""

    analysis = get_completion(prompt, SYSTEM_PROMPT, provider=parsed.provider)

    return {
        "competitor_name": parsed.company_name,
        "competitor_domain": parsed.domain,
        "analysis": analysis,
        "provider_used": parsed.provider,
    }
