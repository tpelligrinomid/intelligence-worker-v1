from datetime import datetime
from typing import Any, Literal, Optional
from pydantic import BaseModel


class CreateJobRequest(BaseModel):
    job_type: Literal["company_research", "competitor_analysis", "industry_research"]
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
    provider: Literal["anthropic", "openai"] = "anthropic"
