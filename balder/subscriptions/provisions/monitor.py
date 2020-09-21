from balder.notifier.utils import initialPayload
import logging

import graphene

from balder.subscriptions.provisions.base import BaseProvisionSubscription
from delt.bouncers.context import BouncerContext
from delt.models import Node, Provision
from delt.pipes import provision_pod_pipe
import uuid

logger = logging.getLogger(__name__)


@initialPayload(lambda context, info, *args, **kwargs: Provision.objects.get(reference=kwargs["reference"]))
class MonitorSubscription(BaseProvisionSubscription):

    class Arguments:
        reference = graphene.String(required=True, description="The Pods unique reference (for the Client)")

    @classmethod
    def accept(cls, context: BouncerContext, root, info, *args, **kwargs):
        
        reference = kwargs.pop("reference")
        try:
            provision = Provision.objects.get(reference=reference)
            if provision.user == context.user:
                logger.info(f"Provision exists. Serving: {provision}")
                return [f'{reference}']
            else:
                raise Exception("This provision is not accessible for the signed in user")
        except Provision.DoesNotExist:
            raise Exception("Provision Does Not Exist")
        
