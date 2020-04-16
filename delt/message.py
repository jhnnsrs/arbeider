import logging.config

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from delt.settingsregistry import get_settings_registry
from delt.serializers import JobSerializer

logger = logging.getLogger(__name__)

def send_to_backend(job):
    backend = job.node.backend
    backjob = get_settings_registry().getHandlerForBackend(backend).on_job(job)

    if backjob is None:
        return JobSerializer(job)
    else:
        return JobSerializer(backjob)
