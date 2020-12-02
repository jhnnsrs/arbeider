from typing import Type
from balder.delt.enums import PodStatus
from vart.serializers import QueueSubscriptionMessageSerializer
from vart.subscriptions.queue import QueueSubscription
from vart.models import VartPod, Volunteer
from delt.consumers.utils import deserialized
import logging

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer

from delt.selector import Selector
from delt.models import Pod, Assignation, Provision, Node
from delt.serializers import  ProvisionMessageSerializer
from delt.pipes import provision_succeeded_pipe
logger = logging.getLogger(__name__)

class HandlerMeta(type):
    pass



channel_layer = get_channel_layer()


class Protocol(object):
    PROVISION_IN = "provision_in"
    PROVISION_SUCCEEDED = "provision_succeeded"


class HandlerSettings:

    def __init__(self, settingsField) -> None:
        # Let that be overridden by the settings#
        # find handler settings
        self.gateway_channel = f"{settingsField}_gateway"
        self.channel_channel = f"{settingsField}_channel"


class Messenger(object):

    def __init__(self, channel, layer=get_channel_layer()) -> None:#
        self.channel = channel
        self.layer = layer

    def contact(self, function: str, message: str, serializer = None):
        if serializer: message = serializer(message).data
        async_to_sync(self.layer.send)(self.channel,{"type": function, "data": message})


class BaseConsumer(SyncConsumer):
    channel = None
    gateway = None 

    def test_message(self, message):
        print(f"{self.channel} is Reachable with {message}")


class HandlerException(Exception):
    pass


def wrappedGatewayHandler(parent):

    class HandlerGatewayConsumer(BaseConsumer):
        channel = Messenger(parent.settings.channel_channel)
        gateway = Messenger(parent.settings.gateway_channel)

        @deserialized(ProvisionMessageSerializer, colapse="provision")
        def provision_succeeded(self, prov: Provision):
            provision_succeeded_pipe(prov)



    return HandlerGatewayConsumer



def wrappedChannelHandler(parent):

    class HandlerChannelConsumer(BaseConsumer):
        channel = Messenger(parent.settings.channel_channel)
        gateway = Messenger(parent.settings.gateway_channel)

        @deserialized(ProvisionMessageSerializer, colapse="provision")
        def provision_in(self, prov: Provision):
            
            pod = parent.provide(prov.node, Selector(prov.subselector))
            pod.active = True
            pod.save()

            # Updating Provision With Pod
            prov.pod = pod
            prov.save()

            self.gateway.contact(Protocol.PROVISION_SUCCEEDED, {"provision": prov}, serializer= ProvisionMessageSerializer)



    return HandlerChannelConsumer



class Handler(metaclass=HandlerMeta):
    ''' Functions prepended by on_ are getting called by our pipes and handle the 
    arnheim interaction, there is not really a need to override them, have a look at the reference implementation of VartHandler'''
    settings = None

    def __init__(self) -> None:
        # Bind should be the provider pass
        assert self.settings is not None, "Please provide a settingsClass to your Handler"

        self.channelMessenger = Messenger(self.settings.channel_channel)
        self.gatewayMessenger = Messenger(self.settings.gateway_channel)

        self._gateway = wrappedGatewayHandler(self)
        self._channel = wrappedChannelHandler(self)

    def getChannel(self) -> Type[BaseConsumer]:
        return self._channel

    def getGateway(self) -> Type[BaseConsumer]:
        return self._gateway


    def on_new_provision(self, provision: Provision):
        # Generally we want to let the Consumer decide how to handle the provision so we send int over 
        self.channelMessenger.contact(Protocol.PROVISION_IN,{"provision": provision}, serializer=ProvisionMessageSerializer)
        print(provision)


    def provide(self, node: Node, selector: Selector) -> Pod:
        # This function is run on the worker Thread! It gets activated from 
        raise NotImplementedError(f"Please overwrite this function in your Handler: {self.__class__.__name__}")


class VartHandler(Handler):
    settings = HandlerSettings("vart")

    def provide(self, node: Node, selector: Selector) -> Pod:
        if selector.is_all():
            # Lets check if there is already a running instance of this Pod? Maybe we can use that template?
            volunteer = Volunteer.objects.filter(node=node, active=True).first()
            pod = VartPod.objects.create(volunteer=volunteer, node=node)
            pod.status = PodStatus.PENDING
            pod.save()
        else:
            raise NotImplementedError("We haven't implemented that yet")    

        logger.info(f"Created POD with Volunteer: {pod.volunteer_id}")
        # We are asking the queued Volunteer if he is accepting the Task
        QueueSubscription.broadcast(group=f"volunteer_{volunteer.id}", payload=QueueSubscriptionMessageSerializer({"pod": pod}).data)
        return pod
