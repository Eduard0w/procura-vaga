import requests
from dotenv import load_dotenv

KEYWORDS = [
    "estágio",
    "estagiário"
]

REMOTE_TERMS = (
    "remote",
    "remoto",
    "remota",
    "home office",
    "homeoffice"
)

REQUEST_TIMEOUT_SECONDS = 20
MAX_PAGES = 100

load_dotenv()


def search_job():
    page_number = 1
    all_jobs_find = []

    while page_number <= MAX_PAGES:
        url = f"https://querovagastech.com.br/api/jobs?page={page_number}&pageSize=20&sort=postedAt%3Adesc"
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        jobs_on_page = data.get("items", [])

        if not jobs_on_page:
            print("vagas acabaram...")
            break

        all_jobs_find.extend(jobs_on_page)
        page_number += 1

    return all_jobs_find


def filter_jobs(jobs):
    filtered_vagas = []

    for job in jobs:
        title = job.get("title", "").lower()
        seniority = job.get("seniority", "").lower()
        location = job.get("location", "").lower()
        work_mode = job.get("workMode", "").lower()

        is_salvador = "salvador" in location
        is_remote = any(
            term in work_mode or term in location
            for term in REMOTE_TERMS
        )

        is_valid_location_or_mode = is_salvador or is_remote

        has_keyword = any(
            keyword in title or keyword in seniority
            for keyword in KEYWORDS
        )

        if is_valid_location_or_mode and has_keyword:
            filtered_vagas.append(job)

    return filtered_vagas
