import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.handlers.base import BaseHandler
from delt.handlers.channels import (ChannelHandler,
                                    ChannelHandlerConfigException,
                                    ChannelHandlerSettings)
from delt.models import Provision
from delt.serializers import JobSerializer

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)


class AutoProviderHandlerSettings(ChannelHandlerSettings):
    provider = "auto"
    provisionConsumer = "auto"


class AutoProviderHandler(BaseHandler):
    settings = AutoProviderHandlerSettings()
    provider = "auto"

    def on_provision_pod(self, provision):
        logger.info(f"Trying to Provision with AUTOHANDLER {provision}")


    def on_new_provision(self, provision: Provision):
        logger.info(f"Trying to Provision with AUTOHANDLER {provision}")
