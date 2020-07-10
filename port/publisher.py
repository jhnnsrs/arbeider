
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from balder.registry import get_registry
from balder.subscriptions.provisions.monitor import MonitorSubscription
from balder.subscriptions.provisions.provide import ProvideSubscription
from delt.models import Job, Pod, Provision
from delt.publishers.base import BasePublisher, BasePublisherSettings
from delt.serializers import (JobSerializer, PodSerializer,
                              ProvisionModelSerializer, ProvisionSerializer)

logger = logging.getLogger(__name__)
JOB_SUBSCRIPTION = "all_jobs"

channel_layer = get_channel_layer()

class PortPublisherSettings(BasePublisherSettings):
    provider = "port"
    onall=True




class PortPublisher(BasePublisher):
    settingsClass = PortPublisherSettings

    def __init_(self):
        super().__init__(self)


    def on_job_updated(self, job: Job):
        logger.info(f"Uppdated Job: {str(job)}")


    def on_provision_succeeded(self, provision: Provision):
        if provision.parent is None:
            logger.info("PortPublisher skips this provision, as it has no Parent, therefore does not originate from within the cluster!")
            return
        if provision.parent.pod.provider == "port":
            channel = "provision-" + str(provision.parent.node.id)
            logger.info(f"Sending succeeded Provision to channel {channel}")
            serialized = ProvisionModelSerializer(provision)
            async_to_sync(channel_layer.send)(channel, {"type": "on_provision_succeeded", "data": serialized.data})
        else:
            logger.info("PortPublisher skips this provision, as it is parent inone of its Provisions")
        

    def on_provision_failed(self, provision):
        channel = "provision-" + provision.node.id
        logger.info(f"Sending failed Provision to channel {channel}")
        serialized = ProvisionModelSerializer(provision)
        async_to_sync(channel_layer.send)(channel, {"type": "on_provision_failed", "data": serialized.data})
