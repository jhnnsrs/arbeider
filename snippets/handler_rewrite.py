from delt.serializers import ProvisionMessageSerializer
from delt.consumers.utils import deserialized
from typing import TypedDict

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from delt.models import Node, Pod, Provision
from vart.models import VartPod, Volunteer
from channels.consumer import SyncConsumer

import logging

logger = logging.getLogger(__name__)








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
        class HandlerConsumer(SyncConsumer):
            
            @deserialized(ProvisionMessageSerializer, colapse="provision")
            def provision_in(this, prov: Provision):
                
                pod = self.provide(prov.node, prov.selector)
                pod.active = True
                pod.save()

                prov.pod = pod
                prov.save()

                return getGateway().contact(ProvisionMessageSerializer({"provision": prov}))



        return HandlerConsumer



    def provide(self, node: Node, selector: Selector) -> Pod:
        # Should return either the Pod or raise an Exception
        raise NotImplementedError("Please override this method in your handler")


    def message_channel(self, channel, message):
        async_to_sync(get_channel_layer().send)(channel,message)



        







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







    




