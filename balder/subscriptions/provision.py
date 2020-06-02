import logging
import uuid

import graphene

from balder.delt_types import NodeType, PodType, UserType
from balder.subscriptions.base import BaseSubscription
from balder.utils import serializerToDict
from delt.bouncers.context import BouncerContext
from delt.context import Context
from delt.models import Node, Pod, Provision
from delt.pipes import provision_pod_pipe
from delt.serializers import PodSerializer, ProvisionSerializer

logger = logging.getLogger(__name__)

class ProvisionSubscription(BaseSubscription):
    node = graphene.Field(NodeType, required=False, description="The Node you Provisioned")
    pod = graphene.Field(PodType,required= False, description="The Provisioned Pod unique Id")
    error = graphene.String(required=False, description="The Provider of this Pod")
    reference = graphene.String(required=False, description="This Provisions reference")
    subselector = graphene.String(required=False, description="This Pods status")
    user = graphene.Field(UserType, required=False, description="This Pods status")
    provider = graphene.String(required=False, description="This Pods status")

    class Arguments:
        node = graphene.ID(required=True, description="The node's id")
        reference = graphene.String(required=False, description="This Pods unique Reference (for the Client)")
        selector = graphene.String(required=False, description="The SelectorString")

    @classmethod
    def subscribe(cls, root, info, *args, **kwargs):
        context = BouncerContext(info=info)

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        nodeid = kwargs.pop("node") if "node" in kwargs else None
        selector = kwargs.pop("selector") if "selector" in kwargs else "__auto__"
        
        try:
            node = Node.objects.get(id=nodeid)
        except Node.DoesNotExist:
            raise Exception("The node you specified does not exist!")

        try:
            provision = Provision.objects.get(reference=reference)
            if provision.node == node:
                logger.info("Reconnecting to already configured Provision")
                return [f'provision_{reference}']
            else:
                raise Exception("This provision already exists is another configuration. Cannot re-assign! Please use different refernce (UUID)")
        except Provision.DoesNotExist:

            logger.info("We are trying to create a new Pod through this Provision")
            provision_pod_pipe(reference, node, selector, context)

        
        return [f"provision_{reference}"]

    @classmethod
    def publish(cls, payload, info, *arg, **kwargs):
        logger.info("Publishing it to the Consumer")
        serializer = ProvisionSerializer(data=payload)
        kwargs = serializerToDict(serializer)
        return cls(**kwargs)