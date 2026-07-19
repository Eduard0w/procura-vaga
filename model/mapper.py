from database.jobs import save_job, job_exists
from .job import Job

def mapper_job_save(filtered_jobs):
    jobs_objects = []
    for job_dict in filtered_jobs:
        # Cria uma instância da classe Job a partir do dicionário
        # Certifique-se de que as chaves do dicionário correspondem aos parâmetros do construtor de Job
        # E que os campos esperados (title, company, url, source, zone) existem no dicionário
        new_job = Job(
            title=job_dict.get("title", "N/A"),
            company=job_dict.get("company", "N/A"),
            url=job_dict.get("applyUrl", "N/A"),
            source=job_dict.get("sourceName", "N/A"), # Assumindo que a API retorna um campo 'source'
            zone=job_dict.get("location", "N/A"), # Assumindo que a API retorna um campo 'zone'
            work_mode=job_dict.get("workMode", "N/A")
        )
        jobs_objects.append(new_job)

    print(jobs_objects) # Agora temos uma lista de objetos Job

    notif_new_job = []

    for jobs in jobs_objects:
        if not job_exists(jobs.url):
            notif_new_job.append(jobs)
            save_job(jobs)

    return notif_new_job
