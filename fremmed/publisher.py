

import logging

from balder.subscriptions.provision import ProvisionSubscription
from balder.registry import get_registry
from delt.models import Job, Pod
from delt.publishers.base import BasePublisher, BasePublisherSettings
from delt.serializers import JobSerializer, PodSerializer
from extensions.fremmed.subscriptions import GateSubscription

logger = logging.getLogger(__name__)
JOB_SUBSCRIPTION = "all_jobs"


class FremmedPublisherSettings(BasePublisherSettings):
    provider = "fremmed"

class FremmedPublisher(BasePublisher):
    settingsClass = FremmedPublisherSettings

    def __init_(self):
        super().__init__(self)


    def on_job_assigned(self, job: Job):
        unique = job.pod.unique
        serialized = JobSerializer(job)
        logger.info(f"Publishing Job to Gate {unique}: {str(job)}")
        GateSubscription.broadcast(group=f"gate_{unique}", payload=serialized.data)


    def on_job_updated(self, job: Job):
        logger.info(f"Uppdated Job: {str(job)}")


    def on_pod_provisioned(self, pod: Pod):
        serialized = PodSerializer(pod)
        ProvisionSubscription.broadcast(group=f"provision_{pod.reference}",payload=serialized.data)

    def on_pod_updated(self, pod: Pod):
        serialized = PodSerializer(pod)
        ProvisionSubscription.broadcast(group=f"provision_{pod.reference}",payload=serialized.data)