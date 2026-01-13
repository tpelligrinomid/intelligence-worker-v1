from app.ai_client import get_completion
from app.models import KickoffQuestionsInput


SYSTEM_PROMPT = """You are an expert B2B marketing strategist preparing for a client kickoff meeting. Your job is to generate insightful, specific questions that will help the marketing team deeply understand the client's business, customers, and competitive landscape.

Generate questions that are:
- Specific to THIS client's industry and situation (not generic)
- Open-ended to encourage detailed responses
- Designed to uncover insights that will inform marketing strategy
- Organized by clear categories

Format your response with clear section headers and numbered questions. Be thorough but focused."""


def process(input_data: dict) -> dict:
    parsed = KickoffQuestionsInput(**input_data)

    prompt = f"""Generate a comprehensive kickoff meeting question list for {parsed.client_name} ({parsed.client_domain}).

CLIENT CONTEXT:
- Industry: Wireless tower infrastructure / telecommunications
- Ideal Customer: {parsed.ideal_customer}
- Sales Cycle: {parsed.sales_cycle}
- Monthly Ad Budget: {parsed.monthly_budget}
- Priorities: {parsed.priorities}
- Past Marketing Success: {parsed.past_success}
- CRM: {parsed.crm}
- Team Members: {parsed.team_members}
- Competitors: {parsed.competitors}

RESEARCH SUMMARY:
{parsed.research_summary[:8000]}

Generate 10-15 specific, insightful questions for EACH of these sections:

### 1. IDEAL CUSTOMERS & SEGMENTATION
Questions to understand their customer segments, buyer personas, decision-makers, geographic focus, and what makes their best customers different from average ones.

### 2. SALES PROCESS & PIPELINE
Questions about how deals progress, common objections, what triggers buying decisions, handoff between marketing and sales, and pipeline visibility.

### 3. COMPETITIVE POSITIONING
Questions about how they win against competitors, why they lose deals, what makes them genuinely different, and how customers perceive them vs. alternatives.

### 4. CONTENT & MESSAGING
Questions about what resonates with their audience, content that has worked, messaging they want to emphasize, and brand voice/tone preferences.

### 5. GOALS & SUCCESS METRICS
Questions about specific targets, how they measure success, what "good" looks like, and priorities for the engagement.

### 6. HISTORICAL CONTEXT & LESSONS
Questions about what they've tried before, what worked/didn't work, any past agency experiences, and institutional knowledge to leverage.

Make questions specific to their tower/wireless infrastructure business, their dual customer base (carriers AND landowners), and their competitive landscape. Avoid generic marketing questions - these should feel tailored to THIS client."""

    questions = get_completion(prompt, SYSTEM_PROMPT, provider=parsed.provider)

    return {
        "client_name": parsed.client_name,
        "questions": questions,
        "provider_used": parsed.provider,
    }
