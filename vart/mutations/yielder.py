from delt.models import Assignation
from vart.types import EndType, MarkType, YieldType
from balder.mutations.base import BaseMutation
from delt.enums import AssignationStatus
import graphene
import logging
logger = logging.getLogger(__name__)
from delt.pipes import assignation_critical_pipe, assignation_done_pipe, assignation_progress_pipe, assignation_yielded_pipe
from graphene.types.generic import GenericScalar
from django.apps import apps



class YieldMutation(BaseMutation):
    Output = YieldType

    class Arguments:
        outputs = GenericScalar(description="The Outputs your Assignation ended with")
        assignation = graphene.ID(required=True, description="The ID for the Assignation")

    @classmethod
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Yield incoming")
        logger.info(f"Initialized by {context.user}")

        logger.info(args)
        
        id = kwargs.pop("assignation")
        outputs = kwargs.pop("outputs")
        #TODO: Check integrity of outputs
        assi = Assignation.objects.get(id=id)
        assi.outputs = outputs
        assi.status = AssignationStatus.YIELD
        assi.save()

        assignation_yielded_pipe(assi)
        return YieldType(registered=True)
