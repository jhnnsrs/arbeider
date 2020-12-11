from balder.delt.inputs import SelectorInput
import logging
import uuid

import graphene

from balder.subscriptions.provisions.base import BaseProvisionSubscription
from delt.models import Node, Provision
from delt.pipes import provision_pod_pipe, republish_provision_pipe

logger = logging.getLogger(__name__)

class ProvideSubscription(BaseProvisionSubscription):

    class Arguments:
        node = graphene.ID(required=True, description="The node's id")
        reference = graphene.String(required=False, description="This Pods unique Reference (for the Client)")
        selector = SelectorInput(required=False, description="The Selector")
        parent = graphene.String(required=False, description="The parent provision")

    @classmethod
    def accept(cls, context, root, info, *args, **kwargs):

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        nodeid = kwargs.pop("node") if "node" in kwargs else None
        selector = kwargs.pop("selector") if "selector" in kwargs else "__auto__"
        parent = kwargs.pop("parent") if "parent" in kwargs else None
        
        try:
            node = Node.objects.get(id=nodeid)
        except Node.DoesNotExist:
            raise Exception("The node you specified does not exist!")

        try:
            provision = Provision.objects.get(reference=reference)
            if provision.node == node:
                logger.info("Reconnecting to already configured Provision")
                republish_provision_pipe(provision)
                return [f'{reference}']
            else:
                raise Exception("This provision already exists is another configuration. Cannot re-assign! Please use different refernce (UUID)")
        except Provision.DoesNotExist:

            logger.info("We are trying to create a new Pod through this Provision")
            provision = provision_pod_pipe(context, reference, node, selector, parent)

        
        return [f"{reference}"]
