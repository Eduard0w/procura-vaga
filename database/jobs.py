from database.db import get_connection
from model.job import Job


def save_job(job: Job):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO jobs (
            title,
            company,
            url,
            source,
            zone
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            job.title,
            job.company,
            job.url,
            job.source,
            job.zone
        )
    )

    conn.commit()
    conn.close()


def job_exists(url: str) -> bool:
    conn = get_connection()

    result = conn.execute(
        "SELECT 1 FROM jobs WHERE url = ?",
        (url,)
    ).fetchone()

    conn.close()

    return result is not None
