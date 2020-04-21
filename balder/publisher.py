

import logging

from balder.schema import JobSubscription
from delt.models import Job
from delt.publishers.base import BasePublisher, BasePublisherSettings
from delt.serializers import JobSerializer

logger = logging.getLogger(__name__)



class BalderPublisherSettings(BasePublisherSettings):
    provider = "balder"

class BalderPublisher(BasePublisher):
    settings = BalderPublisherSettings

    def __init_(self):
        super().__init__(self)


    def on_job_created(self, job: Job):
        logger.info(f"Publishing Job: {str(job)}")
        pod = job.pod
        if pod is not None:
            serialized = JobSerializer(job)
            JobSubscription.broadcast(group="pod_"+str(pod.id), payload=serialized.data)


    def on_job_updated(self, job: Job):
        logger.info(f"Uppdated Job: {str(job)}")