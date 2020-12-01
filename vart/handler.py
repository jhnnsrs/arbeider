from _typeshed import NoneType
from typing import TypedDict, Union

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from delt.handlers.channels import ChannelHandler, ChannelHandlerSettings
from delt.models import Node, Pod
from vart.models import VartPod, Volunteer

import logging

logger = logging.getLogger(__name__)

class PortHandlerSettings(ChannelHandlerSettings):
    provider = "vart"
    provisionConsumer = "vart"


class PortHandler(ChannelHandler):
    settings = PortHandlerSettings()
    provider = "vart"


class HandlerMeta(type):
    pass



class Selector(TypedDict):
    name: str

channel_layer = get_channel_layer()


class HandlerSettings:

    def __init__(self, settingsField) -> None:
        # Let that be overridden by the settings#
        # find handler settings


        self.channel = "vart"



class Handler(metaclass=HandlerMeta):
    settings = HandlerSettings("vart")

    @classmethod
    def contact(cls, message):
        async_to_sync(get_channel_layer().send)(cls.settings.channel,message)

    def __init__(self) -> None:
        # Bind should be the provider pass
        assert self.settings is not None, "Please provide a settingsClass to your Handler"

    def getConsumer(self):
        # The consumer should be able to handle the protocol changes     
        class HandlerConsumer(object):
            
            def onMessage(this, message):
                self.provide("")

        return HandlerConsumer



    def provide(self, node: Node, selector: Selector) -> Pod:
        # Should return either the Pod or raise an Exception
        raise NotImplementedError("Please override this method in your handler")


    def message_channel(self, channel, message):
        async_to_sync(get_channel_layer().send)(channel,message)



        








class HandlerException(Exception):
    pass


class VolunteerNotFoundError(HandlerException):
    pass




class VartHandler(Handler):


    def provide(self, node: Node, selector: Selector) -> Pod:
        
        try:
            volunteer = Volunteer.objects.filter(node=node, active=True).first()
        except Exception as e:
            logger.info("Couldn't find an Active Node")
            try:
                volunteer = Volunteer.objects.filter(node=node, active=False).first()
            except:
                raise VolunteerNotFoundError("We couldn't find a Volunteering Node for this Node")
        
        pod = VartPod.objects.create(volunteer=volunteer)
        return pod


    def assign(self, pod: Pod, inputs: dict):
        return None







    




