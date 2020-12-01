from vart.types import MarkType
from balder.mutations.base import BaseMutation
from balder.delt.enums import PodStatus
import graphene
import logging
logger = logging.getLogger(__name__)


from django.apps import apps



class MarkMutation(BaseMutation):
    Output = MarkType

    class Arguments:
        message = graphene.String(required=True, description="Your message")
        podid = graphene.ID(required=True, description="The ID for the pod")
        level = graphene.Argument(PodStatus)

    @classmethod
    def change(cls, context, root, info, *args, **kwargs):
        logger.warn("Marking incoming")
        logger.info(f"Initialized by {context.user}")

        logger.info(args)
        

        mark = {
            "registered": True
        }


        return MarkType(registered=True)