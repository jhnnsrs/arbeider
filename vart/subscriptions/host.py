from delt.models import Assignation
from vart.types import VartPodType
from vart.serializers import HostSubscriptionMessageSerializer, QueueSubscriptionMessageSerializer
from vart.models import VartPod, Volunteer
from balder.subscriptions.base import BaseSubscription
import graphene
import logging
from balder.delt.enums import PodStatus
from balder.delt.models import AssignationType
from delt.pipes import pod_activated_pipe

logger = logging.getLogger(__name__)

class HostSubscription(BaseSubscription):
    Output = AssignationType



    class Arguments:
        pod = graphene.ID(required=True, description="The pod you want to host")


    @classmethod
    def unsubscribed(cls,*args, **kwargs):
        pod_id = kwargs.pop("pod")

        pod = VartPod.objects.get(id=pod_id)
        pod.status = PodStatus.ERROR
        pod.save()


        logger.warn(f"{pod} has disconnected. Setting Inactive")

    @classmethod
    def announce(cls, context, payload, *arg, **kwargs):
        serialized = HostSubscriptionMessageSerializer(data=payload)
        logger.warn("aebfiubaeiuofnouieabn")
        if serialized.is_valid():
            return serialized.validated_data["assignation"]
        else:
            return None


    @classmethod
    def accept(cls, context, root, info, *args, **kwargs):
        
        pod_id = kwargs.pop("pod")

        pod = VartPod.objects.get(id=pod_id)
        pod.status = PodStatus.ACTIVE
        pod.save()
        pod_activated_pipe(pod)

        logger.warn(f"{pod} is ready for Assignation")

        return [f"vartpod_{pod.id}"]
