

import logging

from balder.registry import get_registry
from balder.subscriptions.provision import ProvisionSubscription
from delt.models import Job, Pod
from delt.publishers.base import BasePublisher, BasePublisherSettings
from delt.serializers import JobSerializer, PodSerializer, ProvisionSerializer

logger = logging.getLogger(__name__)
JOB_SUBSCRIPTION = "all_jobs"


class BalderPublisherSettings(BasePublisherSettings):
    provider = "balder"
    onall=True

class BalderPublisher(BasePublisher):
    settingsClass = BalderPublisherSettings

    def __init_(self):
        super().__init__(self)


    def on_job_assigned(self, job: Job):
        logger.info(f"Publishing Job: {str(job)}")
        node = job.pod.node
        reference = job.reference
        serialized = JobSerializer(job)
        get_registry().getSubscriptionForNode(node).broadcast(group=f"job_{reference}", payload=serialized.data)


    def on_job_updated(self, job: Job):
        logger.info(f"Uppdated Job: {str(job)}")

    def on_provision_succeeded(self, provision):
        serialized = ProvisionSerializer(provision)
        ProvisionSubscription.broadcast(group=f"provision_{provision['reference']}",payload=serialized.data)

    def on_provision_failed(self, provision):
        serialized = ProvisionSerializer(provision)
        ProvisionSubscription.broadcast(group=f"provision_{provision['reference']}",payload=serialized.data)

    def on_pod_pending(self, pod: Pod):
        for provision in pod.provisions.all():
            serialized = ProvisionSerializer(provision)
            ProvisionSubscription.broadcast(group=f"provision_{provision.reference}",payload=serialized.data)

    def on_pod_ready(self, pod: Pod):
        for provision in pod.provisions.all():
            serialized = ProvisionSerializer(provision)
            ProvisionSubscription.broadcast(group=f"provision_{provision.reference}",payload=serialized.data)