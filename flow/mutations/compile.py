from flow.types import ExecutionGraphType
from flow.models import ExecutionGraph
from delt.bouncers.context import bounce
from vart.models import Volunteer
from vart.types import MarkType, VolunteerType
from balder.mutations.base import BaseMutation
import graphene
import logging
logger = logging.getLogger(__name__)


from django.apps import apps



class CompileMutation(BaseMutation):
    Output = ExecutionGraphType

    class Arguments:
        graph = graphene.ID(description="The Graph you want to compile")
        compiler = graphene.ID(description="The Compiler you want to use for this job")

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