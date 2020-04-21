import logging
from delt.models import Job
from delt.publishers.base import BasePublisher, BasePublisherSettings


logger = logging.getLogger(__name__)



class LogPublisherSettings(BasePublisherSettings):
    provider = "log"

class LogPublisher(BasePublisher):
    settings = LogPublisherSettings

    def __init_(self):
        super().__init__(self)


    def on_job_created(self, job: Job):
        logger.info(f"Created Job: {str(job)}")


    def on_job_updated(self, job: Job):
        logger.info(f"Uppdated Job: {str(job)}")