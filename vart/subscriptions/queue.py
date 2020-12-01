from vart.models import Volunteer
from balder.subscriptions.base import BaseSubscription
from balder.delt.models import PodType
import graphene
import logging


logger = logging.getLogger(__name__)

class QueueSubscription(BaseSubscription):
    Output = PodType



    class Arguments:
        volunteer = graphene.ID(required=True, description="Your volunteer identification")
        reference = graphene.String(required=False, description="The pods id")


    @classmethod
    def unsubscribed(cls,*args, **kwargs):
        volunteer_id = kwargs.pop("volunteer")
        volunteer = Volunteer.objects.get(id=volunteer_id)
        volunteer.active = True
        volunteer.save()


        logger.info(f"{volunteer} lost the connection, setting inactive")

    @classmethod
    def announce(cls, context, payload, *arg, **kwargs):
        print(payload)
        return None


    @classmethod
    def accept(cls, context, root, info, *args, **kwargs):
        
        volunteer_id = kwargs.pop("volunteer")

        volunteer = Volunteer.objects.get(id=volunteer_id)
        volunteer.active = True
        volunteer.save()


        logger.info(f"{volunteer} is waiting for Pod")


        return [f"{volunteer.id}"]
