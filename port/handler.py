import logging

from asgiref.sync import async_to_sync
from celery import signature
from channels.layers import get_channel_layer

from delt.handlers.channels import (ChannelHandler,
                                    ChannelHandlerConfigException,
                                    ChannelHandlerSettings)
from delt.models import Pod, Assignation
from delt.serializers import JobSerializer

logger = logging.getLogger(__name__)

class KanalHandlerConfigException(ChannelHandlerConfigException):
    pass

class PortHandlerSettings(ChannelHandlerSettings):
    provider = "port"
    provisionConsumer = "port"


class PortHandler(ChannelHandler):
    settings = PortHandlerSettings()
    provider = "port"

