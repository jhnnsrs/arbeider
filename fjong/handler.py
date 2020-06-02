import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.handlers.channels import (ChannelHandler,
                                    ChannelHandlerConfigException,
                                    ChannelHandlerSettings)
from delt.serializers import JobSerializer

logger = logging.getLogger(__name__)

class KanalHandlerConfigException(ChannelHandlerConfigException):
    pass

class AutoHandlerSettings(ChannelHandlerSettings):
    provider = "auto"
    provisionConsumer = "auto"


class AutoHandler(ChannelHandler):
    settings = AutoHandlerSettings()
    provider = "auto"
