

import logging

from balder.subscriptions import JobSubscription
from delt.models import Job
from delt.publishers.base import BasePublisher, BasePublisherSettings
from delt.serializers import JobSerializer
from balder.registry import get_registry

logger = logging.getLogger(__name__)
JOB_SUBSCRIPTION = "all_jobs"


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
            get_registry().getSubscription(JOB_SUBSCRIPTION).broadcast(group="pod_"+str(pod.id), payload=serialized.data)


    def on_job_updated(self, job: Job):
        logger.info(f"Uppdated Job: {str(job)}")