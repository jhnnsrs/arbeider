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

class VartHandlerEnv(BaseHandlerEnvironment[VartSettings]):
    settingsModel = VartSettings


class VartHandler(BaseHandler):
    env = VartHandlerEnv("vart")

    def provide(self, node: Node, selector: Selector) -> Pod:
        if selector.is_all():
            # Lets check if there is already a running instance of this Pod? Maybe we can use that template?
            volunteer = Volunteer.objects.filter(node=node, active=True).first()
            pod = VartPod.objects.create(volunteer=volunteer, node=node, provider=self.env.provider_name)
            pod.status = PodStatus.PENDING.value
            pod.save()
        else:
            raise NotImplementedError("We haven't implemented that yet")    

        logger.info(f"Created POD with Volunteer: {pod.volunteer_id}")
        # We are asking the queued Volunteer if he is accepting the Task
        QueueSubscription.broadcast(group=f"volunteer_{volunteer.id}", payload=QueueSubscriptionMessageSerializer({"pod": pod}).data)
        return pod


    def assign(self, assignation: Assignation) -> bool:
        HostSubscription.broadcast(group=f"vartpod_{assignation.pod.id}", payload=HostSubscriptionMessageSerializer({"assignation": assignation}).data)
        return True   