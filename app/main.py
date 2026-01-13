from fastapi import FastAPI, HTTPException
from app import database
from app.models import (
    CreateJobRequest,
    CreateJobResponse,
    JobStatusResponse,
    HealthResponse,
)

app = FastAPI(
    title="Intelligence Service",
    description="AI-powered research and analysis service",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy")


@app.post("/jobs", response_model=CreateJobResponse)
async def create_job(request: CreateJobRequest):
    job = database.create_job(
        job_type=request.job_type,
        input_data=request.input,
        callback_url=request.callback_url,
    )

    return CreateJobResponse(
        job_id=job["id"],
        status=job["status"],
    )


@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job(job_id: str):
    job = database.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatusResponse(
        job_id=job["id"],
        status=job["status"],
        output=job.get("output"),
        error=job.get("error"),
        created_at=job["created_at"],
        completed_at=job.get("completed_at"),
    )
