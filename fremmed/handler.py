from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.handler import BaseHandler, BaseHandlerConfigException
from delt.serializers import JobSerializer
from fremmed.provisioner import FremmedProvisioner
import logging

logger = logging.getLogger(__name__)
CHANNELS_JOB_ACTION = "emit_job"

class FremmedHandlerConfigException(BaseHandlerConfigException):
    pass

class FremmedHandler(BaseHandler):
    provisioner = FremmedProvisioner()

    def send_job(self, job, pod):
        serialized = JobSerializer(job)
        path = job.node.frontendnode.path
        logger.info(f"Sending to Path {path} at pod {pod}")
        return job

    def on_outputs(self, outputs, publishers, node_identifier):
        logger.info(f"Received Outputs from Node {node_identifier}")
        raise FremmedHandlerConfigException("Outputs has not yet been defined")
        return super().on_outputs(outputs, publishers)