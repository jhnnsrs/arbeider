from elements.models import  Sample
from elements.types import SampleType
from balder.mutations.base import BaseMutation
import graphene
import logging
logger = logging.getLogger(__name__)



class CreateSampleMutation(BaseMutation):
    Output = SampleType

    class Arguments:
        name = graphene.String(required=True, description="A cleartext description what this representation represents as data")
        experiment = graphene.ID(required=False, description="The Experiment this Sample Belongs to")
    
    @classmethod
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Sample Incoming")
        logger.info(f"Initialized by {context.user}")

        if context.user is None or context.user.username == "AnonymousUser": raise Exception("U need to be signed in for this")

        sample = Sample.objects.create(creator = context.user, **kwargs)

        return sample