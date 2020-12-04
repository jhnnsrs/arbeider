from delt.models import Assignation
from vart.types import EndType, MarkType
from balder.mutations.base import BaseMutation
from balder.delt.enums import AssignationStatus, PodStatus
import graphene
import logging
logger = logging.getLogger(__name__)
from delt.pipes import assignation_critical_pipe, assignation_done_pipe, assignation_progress_pipe
from graphene.types.generic import GenericScalar
from django.apps import apps



class EndMutation(BaseMutation):
    Output = EndType

    class Arguments:
        outputs = GenericScalar(description="The Outputs your Assignation ended with")
        assignation = graphene.ID(required=True, description="The ID for the Assignation")

    @classmethod
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Marking incoming")
        logger.info(f"Initialized by {context.user}")

        logger.info(args)
        
        id = kwargs.pop("assignation")
        outputs = kwargs.pop("outputs")
        #TODO: Check integrity of outputs
        assi = Assignation.objects.get(id=id)
        assi.outputs = outputs
        assi.status = AssignationStatus.DONE.value
        assi.save()

        assignation_done_pipe(assi)
        return MarkType(registered=True)
