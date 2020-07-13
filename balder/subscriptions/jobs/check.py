import logging

import graphene

from balder.subscriptions.jobs.base import BaseAssignationSubscription
from delt.bouncers.context import BouncerContext
from delt.models import Assignation
import uuid

logger = logging.getLogger(__name__)

class CheckSubscription(BaseAssignationSubscription):

    class Arguments:
        reference = graphene.String(required=True, description="The Jobs unique reference (for the Client)")

    @classmethod
    def accept(cls, context: BouncerContext, root, info, *args, **kwargs):
        
        reference = kwargs.pop("reference")
        try:
            assignation = Assignation.objects.get(reference=reference)
            if assignation.user == context.user:
                logger.info(f"Job exists. Serving: {assignation}")
                return [f'{reference}']
            else:
                raise Exception("This Job is not accessible for the signed in user")
        except Assignation.DoesNotExist:
            raise Exception("Job Does Not Exist")
        
