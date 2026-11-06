from database.jobs import job_exists
from .job import Job


def _to_job(job_dict):
    return Job(
        title=job_dict.get("title", "N/A"),
        company=job_dict.get("company", "N/A"),
        url=job_dict.get("applyUrl", "N/A"),
        source=job_dict.get("sourceName", "N/A"),
        zone=job_dict.get("location", "N/A"),
        work_mode=job_dict.get("workMode", "N/A")
    )


def get_new_jobs(filtered_jobs):
    new_jobs = []
    seen_urls = set()

    for job_dict in filtered_jobs:
        job = _to_job(job_dict)

        if not job.url or job.url == "N/A":
            continue
        if job.url in seen_urls:
            continue

        seen_urls.add(job.url)

        if not job_exists(job.url):
            new_jobs.append(job)

    return new_jobs
