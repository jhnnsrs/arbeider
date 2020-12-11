from vart.selector import VartSelector
from vart.serializers import HostSubscriptionMessageSerializer
from vart.subscriptions.host import HostSubscription
from vart.subscriptions.queue import QueueSubscription, QueueSubscriptionMessageSerializer
from logging import Logger
from vart.models import VartPod, VartSettings, Volunteer
from delt.selector import Selector
from delt.models import Assignation, Node, Pod
from delt.handlers.newbase import BaseHandler
from delt.handlers.env import BaseHandlerEnvironment
from typing import Protocol
from balder.delt.enums import PodStatus
import logging


logger = logging.getLogger(__name__)

class VartProtocol(Protocol):
    pass

class VartHandlerEnv(BaseHandlerEnvironment[VartSettings, VartSelector]):
    settingsModel = VartSettings
    selectorClass = VartSelector



class VartHandler(BaseHandler):
    env = VartHandlerEnv("vart")

    
    def provide(self, node: Node, selector: dict) -> Pod:

        if "volunteer" in selector:
            volunteer = selector["volunteer"]    
        elif "all" in selector and selector["all"]:
            volunteer = Volunteer.objects.filter(node=node, active=True).first()
        else:
            raise NotImplementedError("We haven't implemented that yet")    
        

        pod = VartPod.objects.create(volunteer=volunteer, node=node, provider=self.env.provider_name)
        pod.status = PodStatus.PENDING.value
        pod.save()


        logger.info(f"Created POD with Volunteer: {pod.volunteer_id}")
        # We are asking the queued Volunteer if he is accepting the Task
        QueueSubscription.broadcast(group=f"volunteer_{volunteer.id}", payload=QueueSubscriptionMessageSerializer({"pod": pod}).data)
        return pod

    def assign(self, assignation: Assignation) -> bool:
        HostSubscription.broadcast(group=f"vartpod_{assignation.pod.id}", payload=HostSubscriptionMessageSerializer({"assignation": assignation}).data)
        return True   