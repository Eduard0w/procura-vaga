import requests
from dotenv import load_dotenv
# import os

KEYWORDS = [
    "estágio",
    "estagiário"
]

load_dotenv()

# URL = os.getenv("URL_API")

def search_job():
    page_number = 1
    all_jobs_find = []

    while True:
        url = f"https://querovagastech.com.br/api/jobs?page={page_number}&pageSize=20&sort=postedAt%3Adesc"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        jobs_on_page = data["items"]

        if not jobs_on_page:
            print("vagas acabaram...")
            break
        else:
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
        is_remote = "remote" in work_mode

        is_valid_location_or_mode = is_salvador or is_remote

        has_keyword = False
        for keyword in KEYWORDS:
            if keyword.lower() in title or keyword.lower() in seniority:
                has_keyword = True
                break

        if is_valid_location_or_mode and has_keyword:
            filtered_vagas.append(job)

    return filtered_vagas
