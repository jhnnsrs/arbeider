import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.constants.lifecycle import *
from delt.handlers.base import BaseHandlerConfigException
from delt.handlers.channels import ChannelHandler, ChannelHandlerSettings
from delt.models import Job
from delt.registry import get_delt_registry
from delt.serializers import JobSerializer
from fremmed.models import FrontendPod
from fremmed.serializers import ActivationSerializer

logger = logging.getLogger(__name__)
ACTIVATE_POD_ACTION = "activate_pod"
channel_layer = get_channel_layer()

class FremmedHandlerConfigException(BaseHandlerConfigException):
    pass



class FremmedHandlerSettings(ChannelHandlerSettings):
    provider = "channel"
    provisionConsumer = "fremmed"
    jobConsumer = "fremmedjob"

    

class FremmedHandler(ChannelHandler):
    settings = FremmedHandlerSettings()
    provider = "fremmed"

    def on_activate_pod(self, pod, **kwargs):
        serialized = ActivationSerializer({"pod": pod, "status": POD_ACTIVE})
        channel = self.settings.provisionConsumer
        logger.info(f"Sending Activation to Provisioner at {channel}")
        async_to_sync(channel_layer.send)(channel, {"type": "activate_pod", "data": serialized.data})

    def on_slot_in(self, **kwargs):
        logger.info("Validation")
        gate = kwargs["gate"]
        job = kwargs["job"]
        pod = FrontendPod.objects.get(unique=gate)
        job = Job.objects.get(unique=job)
        config = get_delt_registry().getConfigForIdentifier(pod.node.identifier)
        serialized = config.outputs(data=kwargs["outputs"])
        if serialized.is_valid(raise_exception=True):
            outputs = serialized.validated_data
            job.status = "Has Output"
            job.outputs = outputs
            job.save()
            serialized = JobSerializer(job)
            async_to_sync(channel_layer.send)("gateway", {"type": "job_updated", "data": serialized.data})
            

            logger.info(f"Received Inputs for Gate {kwargs['gate']}")