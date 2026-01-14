from app.ai_client import get_completion
from app.models import KickoffQuestionsInput


SYSTEM_PROMPT = """You are an expert B2B marketing strategist preparing for a client kickoff meeting. Your job is to generate insightful, specific questions that will help the marketing team deeply understand the client's business, customers, and competitive landscape.

Generate questions that are:
- Specific to THIS client's industry and situation (not generic)
- Open-ended to encourage detailed responses
- Designed to uncover insights that will inform marketing strategy
- Reference the client and competitors BY NAME

Format your response with clear section headers (### 1., ### 2., etc.) and numbered questions under each. Be thorough but focused."""


def process(input_data: dict) -> dict:
    parsed = KickoffQuestionsInput(**input_data)

    prompt = f"""Generate a kickoff meeting agenda for {parsed.client_name} ({parsed.client_domain}).

KEY CONTEXT:
- Ideal Customer: {parsed.ideal_customer}
- Sales Cycle: {parsed.sales_cycle}
- Budget: {parsed.monthly_budget}/mo
- Priorities: {parsed.priorities}
- Past Success: {parsed.past_success}
- Competitors: {parsed.competitors}
- CRM: {parsed.crm}
- Team: {parsed.team_members}

RESEARCH SUMMARY:
{parsed.research_summary[:8000]}

Generate 10-15 specific questions for each section:

### 1. YOUR IDEAL CUSTOMERS
(segmentation, buyer groups, stakeholders, best customers, geographic focus, new vs existing business)

### 2. YOUR PRIMARY PRODUCTS & SOLUTIONS
(key benefits, ROI, pricing, implementation, support model, popular features)

### 3. YOUR DIFFERENTIATORS
(vs {parsed.competitors} - what wins deals, proof points, weaknesses)

### 4. MARKETING INFRASTRUCTURE
(CRM management, team capacity, tech stack, reporting, automation)

### 5. MARKETING STRATEGIES
(past efforts, Google Ads performance, landing pages, what worked/didn't)

### 6. STRATEGIC PRIORITIES
(the priorities listed above - where goals came from, success metrics, what makes this a win)

Make questions specific to {parsed.client_name} and reference competitors by name."""

    questions = get_completion(prompt, SYSTEM_PROMPT, provider=parsed.provider)

    return {
        "client_name": parsed.client_name,
        "questions": questions,
        "provider_used": parsed.provider,
    }
