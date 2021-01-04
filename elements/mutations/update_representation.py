from elements.models import Representation
from delt.models import Assignation
from elements.types import RepresentationType
from vart.types import MarkType
from balder.mutations.base import BaseMutation
import graphene
import logging
logger = logging.getLogger(__name__)



class UpdateRepresentationMutation(BaseMutation):
    Output = RepresentationType

    class Arguments:
        rep = graphene.ID(required=True, description="Which sample does this representation belong to")
    
    @classmethod
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Update Incoming")

        rep = Representation.objects.get(id=kwargs.pop("rep"))
        rep.save()

        return rep