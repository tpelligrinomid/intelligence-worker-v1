import time
import traceback
import httpx
from app import database
from app.jobs import company_research, competitor_analysis, industry_research


JOB_HANDLERS = {
    "company_research": company_research.process,
    "competitor_analysis": competitor_analysis.process,
    "industry_research": industry_research.process,
}

POLL_INTERVAL = 5


def process_job(job: dict) -> None:
    job_id = job["id"]
    job_type = job["job_type"]
    input_data = job["input"]
    callback_url = job.get("callback_url")

    print(f"Processing job {job_id} of type {job_type}")

    if not database.claim_job(job_id):
        print(f"Job {job_id} was already claimed by another worker")
        return

    try:
        handler = JOB_HANDLERS.get(job_type)
        if not handler:
            raise ValueError(f"Unknown job type: {job_type}")

        output = handler(input_data)
        database.complete_job(job_id, output)
        print(f"Job {job_id} completed successfully")

        if callback_url:
            send_callback(callback_url, job_id, "completed", output=output)

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"Job {job_id} failed: {error_msg}")
        traceback.print_exc()
        database.fail_job(job_id, error_msg)

        if callback_url:
            send_callback(callback_url, job_id, "failed", error=error_msg)


def send_callback(url: str, job_id: str, status: str, output: dict = None, error: str = None) -> None:
    try:
        payload = {
            "job_id": job_id,
            "status": status,
        }
        if output:
            payload["output"] = output
        if error:
            payload["error"] = error

        response = httpx.post(url, json=payload, timeout=30.0)
        print(f"Callback sent to {url}: {response.status_code}")
    except Exception as e:
        print(f"Failed to send callback to {url}: {e}")


def run_worker():
    print("Starting worker...")

    while True:
        try:
            pending_jobs = database.get_pending_jobs(limit=1)

            for job in pending_jobs:
                process_job(job)

        except Exception as e:
            print(f"Error polling for jobs: {e}")
            traceback.print_exc()

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run_worker()
