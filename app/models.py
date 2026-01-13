from datetime import datetime
from typing import Any, Literal, Optional
from pydantic import BaseModel


class CreateJobRequest(BaseModel):
    job_type: Literal["company_research", "competitor_analysis", "industry_research", "kickoff_questions"]
    input: dict[str, Any]
    callback_url: Optional[str] = None


class CreateJobResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    output: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class HealthResponse(BaseModel):
    status: str


# Input models for specific job types
class CompanyResearchInput(BaseModel):
    company_name: str
    domain: str
    provider: Literal["anthropic", "openai"] = "anthropic"


class CompetitorAnalysisInput(BaseModel):
    company_name: str
    domain: str
    client_context: str
    provider: Literal["anthropic", "openai"] = "anthropic"


class IndustryResearchInput(BaseModel):
    company_name: str
    company_description: str
    icp_details: str
    scraped_content: Optional[str] = None  # Client + competitor website content for context
    provider: Literal["anthropic", "openai"] = "anthropic"


class KickoffQuestionsInput(BaseModel):
    client_name: str
    client_domain: str
    ideal_customer: str
    sales_cycle: str
    monthly_budget: str
    priorities: str
    past_success: str
    crm: str
    team_members: str
    competitors: str
    research_summary: str  # Combined research from company, industry, competitor analysis
    provider: Literal["anthropic", "openai"] = "anthropic"
