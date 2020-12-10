from delt.models import Assignation
from vart.types import MarkType
from balder.mutations.base import BaseMutation
from delt.enums import AssignationStatus
from balder.delt.enums import AssignationStatusEnum 
import graphene
import logging
logger = logging.getLogger(__name__)
from delt.pipes import assignation_critical_pipe, assignation_progress_pipe

from django.apps import apps



class MarkMutation(BaseMutation):
    Output = MarkType

    class Arguments:
        message = graphene.String(required=True, description="Your message")
        assignation = graphene.ID(required=True, description="The ID for the pod")
        level = graphene.Argument(AssignationStatusEnum)

    @classmethod
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Marking incoming")
        logger.info(f"Initialized by {context.user}")

        logger.info(args)
        
        id = kwargs.pop("assignation")
        level = kwargs.pop("level")
        message = kwargs.pop("message")


        if level == AssignationStatus.CRITICAL:
            assi = Assignation.objects.get(id=id)
            assi.outputs = {}
            assi.status = AssignationStatus.CRITICAL
            assi.save()

            assignation_critical_pipe(assi)
            return MarkType(registered=True)

        else:
            assi = Assignation.objects.get(id=id)
            assi.message = message
            assi.status = level
            assi.save()

            assignation_progress_pipe(assi)

        return MarkType(registered=True)