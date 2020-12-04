from elements.models import Representation
from delt.models import Assignation
from elements.types import RepresentationType
from vart.types import MarkType
from balder.mutations.base import BaseMutation
import graphene
import logging
logger = logging.getLogger(__name__)



class CreateRepresentationMutation(BaseMutation):
    Output = RepresentationType

    class Arguments:
        sample = graphene.ID(required=True, description="Which sample does this representation belong to")
        name = graphene.String(required=True, description="A cleartext description what this representation represents as data")
    
    @classmethod
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Represetation Incoming")
        logger.info(f"Initialized by {context.user}")

        sampleid = kwargs.pop("sample")
        name = kwargs.pop("name")
        
        rep = Representation.objects.create(name=name, sample_id = sampleid, creator=context.user)

        return rep