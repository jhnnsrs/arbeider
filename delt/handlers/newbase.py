from delt.handlers.env import BaseHandlerEnvironment
from delt.handlers.protocol import Protocol
from delt.handlers.consumers.basegateway import BaseGatewayConsumer
from delt.handlers.messenger import Messenger
from typing import Type
from vart.subscriptions.host import HostSubscription
from delt.consumers.utils import deserialized
import logging

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer
from delt.handlers.consumers.basehandler import BaseHandlerConsumer
from delt.selector import Selector
from delt.models import Pod, Assignation, Provision, Node, Provider, ProviderSettings
from delt.serializers import  AssignationMessageSerializer, ProvisionMessageSerializer
from delt.pipes import assignation_succeeded_pipe, provision_succeeded_pipe
logger = logging.getLogger(__name__)

class HandlerMeta(type):
    pass



channel_layer = get_channel_layer()





def wrappedGatewayHandler(parent, baseClass):

    class HandlerGatewayConsumer(baseClass):
        handler = parent
        channel = Messenger(parent.env.getChannelChannelName())
        gateway = Messenger(parent.env.getGatewayChannelName())


    return HandlerGatewayConsumer



def wrappedChannelHandler(parent, baseClass):

    class HandlerChannelConsumer(baseClass):
        handler = parent
        channel = Messenger(parent.env.getChannelChannelName())
        gateway = Messenger(parent.env.getGatewayChannelName())


    return HandlerChannelConsumer



class BaseHandler(metaclass=HandlerMeta):
    ''' Functions prepended by on_ are getting called by our pipes and handle the 
    arnheim interaction, there is not really a need to override them, have a look at the reference implementation of VartHandler'''
    env: BaseHandlerEnvironment = None
    handlerClass = BaseHandlerConsumer
    gatewayClass = BaseGatewayConsumer

    def __init__(self) -> None:
        # Bind should be the provider pass
        assert self.env is not None, "Please provide an Environment to your Handler"

        self.channelMessenger = Messenger(self.env.getChannelChannelName())
        self.gatewayMessenger = Messenger(self.env.getGatewayChannelName())

        assert issubclass(self.handlerClass, BaseHandlerConsumer), "Please provide a handler that subclasses BaseHandlerConsumer"
        assert issubclass(self.gatewayClass, BaseGatewayConsumer), "Please provide a gateway that subcasses BaseGatewayConsumer"

        self._gateway = wrappedGatewayHandler(self, self.gatewayClass)
        self._channel = wrappedChannelHandler(self, self.handlerClass)
        self.settings = self.env.getSettings()



    def getChannel(self) -> Type[BaseHandlerConsumer]:
        return self._channel

    def getGateway(self) -> Type[BaseGatewayConsumer]:
        return self._gateway


    def on_new_provision(self, provision: Provision):
        # Generally we want to let the Consumer decide how to handle the provision so we send int over 
        self.channelMessenger.contact(Protocol.PROVISION_IN,{"provision": provision}, serializer=ProvisionMessageSerializer)

    def on_new_assignation(self, assignation: Assignation):
        self.channelMessenger.contact(Protocol.ASSIGNATION_IN,{"assignation": assignation}, serializer=AssignationMessageSerializer)


    def on_assign_job(self, assignation: Assignation):
        # Backward compatibiliy
        return self.on_new_assignation(assignation)
        
        

    def provide(self, node: Node, selector: Selector) -> Pod:
        # This function is run on the worker Thread! It gets activated from 
        raise NotImplementedError(f"Please overwrite this function in your Handler: {self.__class__.__name__}")

    def assign(self, assignation: Assignation) -> bool:
        raise NotImplementedError(f"Please overwrite this function in your Handler: {self.__class__.__name__}")
