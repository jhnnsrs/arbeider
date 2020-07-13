
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
from port.utils import provision_channel_from_id, assignation_channel_from_id

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

    def is_responsible(self, provision):
        if provision.parent is None:
            logger.info("PortPublisher skips this provision, as it has no Parent, therefore does not originate from within the cluster!")
            return False
        if provision.parent.pod.provider == "port":
            return True
        return False

    def send_provision_to_portlayer(self, provision, function):
        channel = provision_channel_from_id(provision.parent.pod.id)
        logger.info(f"Sending succeeded Provision to channel {channel}")
        serialized = ProvisionModelSerializer(provision)
        async_to_sync(channel_layer.send)(channel, {"type": function, "data": serialized.data})


    def on_provision_succeeded(self, provision: Provision):
        if self.is_responsible(provision):
           self.send_provision_to_portlayer(provision, "on_provision_succeeded")
        

    def on_provision_failed(self, provision):
        if self.is_responsible(provision):
           self.send_provision_to_portlayer(provision, "on_provision_failed")
