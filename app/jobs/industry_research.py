from app.ai_client import get_completion
from app.models import IndustryResearchInput


SYSTEM_PROMPT = """You are an expert market research analyst. Your task is to provide comprehensive industry and market insights based on the company and ICP information provided.

Provide your analysis in a structured format covering:
1. Industry Overview
2. Market Size and Growth Trends
3. Key Industry Drivers
4. Major Challenges and Pain Points
5. Regulatory Considerations
6. Technology Trends
7. Competitive Landscape Overview
8. Target Audience Insights (based on ICP)
9. Market Opportunities
10. Strategic Recommendations

Be thorough and provide actionable market intelligence."""


def process(input_data: dict) -> dict:
    parsed = IndustryResearchInput(**input_data)

    prompt = f"""Provide comprehensive industry and market research for the following company:

Company Name: {parsed.company_name}

Company Description:
{parsed.company_description}

Ideal Customer Profile (ICP) Details:
{parsed.icp_details}

Based on this information, provide a comprehensive industry research report that will help this company understand their market, target audience, and strategic opportunities."""

    analysis = get_completion(prompt, SYSTEM_PROMPT, provider=parsed.provider, max_tokens=6000)

    return {
        "company_name": parsed.company_name,
        "analysis": analysis,
        "provider_used": parsed.provider,
    }
