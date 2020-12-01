from vart.models import Volunteer
from vart.types import MarkType, VolunteerType
from balder.mutations.base import BaseMutation
from balder.delt.enums import PodStatus
import graphene
import logging
logger = logging.getLogger(__name__)



from django.apps import apps



class VolunteerMutation(BaseMutation):
    Output = VolunteerType

    class Arguments:
        node = graphene.ID(description="The Node you want to voluneer for pod")
        nodes = graphene.List(graphene.ID, description="The Nodes you want to volunteer for")

    @classmethod
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Marking incoming")
        logger.info(f"Initialized by {context.user}")
        
        volunteer = Volunteer.objects.create(node_id=int(kwargs["node"]), active=False)

        return volunteer