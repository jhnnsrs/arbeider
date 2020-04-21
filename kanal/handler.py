import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.handler import BaseHandler, BaseHandlerConfigException
from delt.serializers import JobSerializer
from kanal.provisioner import KanalProvisioner

CHANNELS_JOB_ACTION = "emit_job"
channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)

class KanalHandlerConfigException(BaseHandlerConfigException):
    pass


class KanalHandler(BaseHandler):
    provisioner = KanalProvisioner()

    def send_job(self, job, pod):
        serialized = JobSerializer(job)
        channel = job.pod.kanalpod.channel
        logger.info(f"Sending to channel {channel}")
        async_to_sync(channel_layer.send)(channel, {"type": CHANNELS_JOB_ACTION, "data": serialized.data})
        return job

    def on_outputs(self, outputs, publishers, node_identifier):
        logger.info(f"Received Outputs from Node {node_identifier}")
        raise KanalHandlerConfigException("Outputs has not yet been defined")
        return super().on_outputs(outputs, publishers)