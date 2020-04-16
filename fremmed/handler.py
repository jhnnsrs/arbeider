from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.handler import BaseHandler
from delt.serializers import JobSerializer

CHANNELS_JOB_ACTION = "emit_job"
channel_layer = get_channel_layer()

class FremmedHandler(BaseHandler):

    def on_job(self, job):
        serialized = JobSerializer(job)
        channel = job.node.backendnode.channelsnode.channel
        logger.info(f"Sending to channel {channel}")
        async_to_sync(channel_layer.send)(channel, {"type": CHANNELS_JOB_ACTION, "data": serialized.data})
        return job

    def on_outputs(self, outputs, publishers, node_identifier):
        logger.info(f"Received Outputs from Node {node_identifier}")
        return super().on_outputs(outputs, publishers)