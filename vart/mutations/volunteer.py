from delt.bouncers.context import bounce
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
        name = graphene.String(description="How would you like to be identifier for us?")
        version = graphene.String(description="Which audience are you targeting?")
        nodes = graphene.List(graphene.ID, description="The Nodes you want to volunteer for")


    @classmethod
    @bounce(accessible=[])
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Volunteering incoming")
        logger.info(f"Initialized by {context.user}")

        name = kwargs.pop("name")
        version = kwargs.pop("version")
        node_id = int(kwargs.pop("node"))

        try:
            return Volunteer.objects.get(name=name, node_id=node_id, version=version)
        except:
            volunteer = Volunteer.objects.create(node_id=node_id, active=False, version=version, name=name, creator=context.user)

        return volunteer