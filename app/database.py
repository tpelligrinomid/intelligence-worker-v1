import os
from datetime import datetime
from typing import Optional
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

_client: Optional[Client] = None


def get_client() -> Client:
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


def create_job(job_type: str, input_data: dict, callback_url: Optional[str] = None) -> dict:
    client = get_client()
    data = {
        "job_type": job_type,
        "status": "pending",
        "input": input_data,
        "callback_url": callback_url,
    }
    result = client.table("jobs").insert(data).execute()
    return result.data[0]


def get_job(job_id: str) -> Optional[dict]:
    client = get_client()
    result = client.table("jobs").select("*").eq("id", job_id).execute()
    return result.data[0] if result.data else None


def get_pending_jobs(limit: int = 10) -> list[dict]:
    client = get_client()
    result = (
        client.table("jobs")
        .select("*")
        .eq("status", "pending")
        .order("created_at")
        .limit(limit)
        .execute()
    )
    return result.data


def claim_job(job_id: str) -> bool:
    client = get_client()
    result = (
        client.table("jobs")
        .update({"status": "processing", "started_at": datetime.utcnow().isoformat()})
        .eq("id", job_id)
        .eq("status", "pending")
        .execute()
    )
    return len(result.data) > 0


def complete_job(job_id: str, output: dict) -> None:
    client = get_client()
    client.table("jobs").update({
        "status": "completed",
        "output": output,
        "completed_at": datetime.utcnow().isoformat(),
    }).eq("id", job_id).execute()


def fail_job(job_id: str, error: str) -> None:
    client = get_client()
    client.table("jobs").update({
        "status": "failed",
        "error": error,
        "completed_at": datetime.utcnow().isoformat(),
    }).eq("id", job_id).execute()
