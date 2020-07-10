import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from celery import signature
from delt.models import Pod

from delt.handlers.channels import (ChannelHandler,
                                    ChannelHandlerConfigException,
                                    ChannelHandlerSettings)
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


    def on_assign_job(self, reference: str, pod: Pod, inputs: dict, user):
        assignation = {
            "reference": reference,
            "pod": pod,
            "inputs": inputs,
            "user": user,
            "provider": self.provider
        }
        channel = self.settings.jobConsumer
