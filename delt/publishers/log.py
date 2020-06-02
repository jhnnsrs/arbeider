import logging
from delt.models import Job
from delt.publishers.base import BasePublisher, BasePublisherSettings


logger = logging.getLogger(__name__)



class LogPublisherSettings(BasePublisherSettings):
    provider = "log"

class LogPublisher(BasePublisher):
    settingsClass = LogPublisherSettings

    def __init_(self):
        super().__init__(self)

    def on_pod_provisioned(self, pod):
        logger.info(f"Provisioned Pod {pod}")

    def on_pod_updated(self, pod):
        logger.info(f"Updated Pod {pod.id}")

    def on_job_created(self, job: Job):
        logger.info(f"Created Job: {str(job)}")


    def on_job_updated(self, job: Job):
        logger.info(f"Uppdated Job: {str(job)}")

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            logger.info(f"Received {args} on Event {name}")
        
        return wrapper