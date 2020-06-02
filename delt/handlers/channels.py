import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from delt.consumers.provisioner import ProvisionConsumer
from delt.consumers.utils import (send_assignation_to_channel,
                                  send_provision_to_channel)
from delt.context import Context
from delt.handlers.base import (BaseHandler, BaseHandlerException,
                                BaseHandlerSettings)
from delt.models import Job, Node, Pod
from delt.serializers import (AssignationSerializer,
                              JobSerializer, ProvisionSerializer)
from delt.settingsregistry import get_settings_registry

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()

PROVISION_ACTION = "on_provision_pod"
ACTIVATION_ACTION = "on_activate_pod"
JOB_QUEUE_ACTION = "on_assign_job"

class ChannelHandlerException(BaseHandlerException):
    pass


class ChannelHandlerConfigException(BaseHandlerException):
    pass

class ChannelHandlerSettings(BaseHandlerSettings):
    provider = "channel"
    provisionConsumer = None
    jobConsumer = None

    def __init__(self, *args, **kwargs):
        if self.provisionConsumer is None: raise ChannelHandlerConfigException("Please specify a provisionConsumer")
        super().__init__(*args, **kwargs)


class ChannelHandler(BaseHandler):
    """ If your Handler relies on async work put it in a Consumer and let its rest here"""
    provider = None
    settings: ChannelHandlerSettings = None
    autoPassThrough = False

    def __init__(self):
        if self.settings.provisionConsumer is None:
            raise ChannelHandlerException("Please specify a path to the provisionConsumer in your Channelhandler")
        logger.debug(f"Registering Handler {self.__class__.__name__}")
        super().__init__()

    def on_provide_pod(self, reference: str, node: Node, subselector: str, user):
        provision = {
            "reference": reference,
            "node": node,
            "subselector": subselector, 
            "user": user,
            "provider": self.provider
            }
        channel = self.settings.provisionConsumer
        send_provision_to_channel(channel, provision)

    def on_assign_job(self, reference: str, pod: Pod, inputs: dict, user):
        assignation = {
            "reference": reference,
            "pod": pod,
            "inputs": inputs,
            "user": user,
            "provider": self.provider
        }
        channel = self.settings.jobConsumer
        send_assignation_to_channel(channel, assignation)
