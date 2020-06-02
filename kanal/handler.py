import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.handlers.channels import (ChannelHandler,
                                    ChannelHandlerConfigException,
                                    ChannelHandlerSettings)
from delt.serializers import JobSerializer

CHANNELS_JOB_ACTION = "emit_job"
channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)

class KanalHandlerConfigException(ChannelHandlerConfigException):
    pass

class KanalHandlerSettings(ChannelHandlerSettings):
    provider = "kanal"
    provisionConsumer = "kanal"
    jobConsumer = "kanaljob"


class KanalHandler(ChannelHandler):
    settings = KanalHandlerSettings()
    provider = "kanal"
