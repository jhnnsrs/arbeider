import logging.config

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.models import Job
from delt.context import Context
from delt.serializers import JobSerializer
from delt.settingsregistry import get_settings_registry

logger = logging.getLogger(__name__)

def send_to_backend(job: Job, context: Context):
    backend = job.pod.provider
    handler = get_settings_registry().getHandlerForBackend(backend)
    
    job = handler.on_job(job, context)
    return JobSerializer(job)
