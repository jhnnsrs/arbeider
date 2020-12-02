
from vart.serializers import QueueSubscriptionMessageSerializer
from django.utils.translation import activate
from vart.handler import VartHandlerSettings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from delt.consumers.gateway import channel_layer
import logging
from port.utils import assignation_channel_from_id

from delt import selector as selectors
from delt.consumers.provisioner import ProvisionConsumer
from delt.models import Assignation
from delt.constants.lifecycle import POD_PENDING
from delt.serializers import AssignationModelSerializer, PodSerializer
from vart.models import Volunteer, VartPod
from vart.subscriptions.queue import QueueSubscription


logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()


class VartProvisionError(Exception):
    pass



class Selector(object):

    def __init__(self, subselector: str) -> None:
        self.subselector = subselector

    def is_all(self) -> bool:
        return selectors.all(self.subselector)

    def is_new(self) -> bool:
        return selectors.new(self.subselector)


    






class VartProvision(ProvisionConsumer):
    settings = VartHandlerSettings()
    provider = "vart"

    def get_pod(self, provision):
        logger.info(f"Received {provision}")

        # Are we provisioning a Flow???
        node = provision.node
        selector = Selector(provision.subselector)

        if selector.is_all():
            # Lets check if there is already a running instance of this Pod? Maybe we can use that template?
            volunteer = Volunteer.objects.filter(node=node, active=True).first()
            pod = VartPod.objects.create(volunteer=volunteer, node=node)
            pod.status = POD_PENDING
            pod.save()

            QueueSubscription.publish(group=f"volunteer_{volunteer.id}", payload=QueueSubscriptionMessageSerializer({"pod": pod}).data)
        else:
            raise NotImplementedError("We haven't implemented that yet")    

        logger.info(f"Created POD with Volunteer: {pod.volunteer_id}")
        logger.info(f"Created POD with PROVISION: {provision.id}")
        return pod


    def assign_inputs(self, assignation: Assignation):

        pod = assignation.pod
        assignation_channel= assignation_channel_from_id(pod.id)
        serialized = AssignationModelSerializer(assignation)
        logger.info(f"Sending Assignation: {assignation_channel}")
        async_to_sync(channel_layer.send)(assignation_channel,{"type": "assign", "data" : serialized.data})

        
