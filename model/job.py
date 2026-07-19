# models/job.py

class Job:

    def __init__(
        self,
        title,
        company,
        url,
        source,
        zone,
        work_mode
    ):
        self.title = title
        self.company = company
        self.url = url
        self.source = source
        self.zone = zone
        self.work_mode = work_mode
