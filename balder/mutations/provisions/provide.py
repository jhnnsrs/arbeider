from balder.delt.inputs import SelectorInput
import logging
import uuid

import graphene

from balder.delt.models import  ProvisionType
from balder.mutations.base import BaseMutation
from delt.models import Node
from delt.pipes import provision_pod_pipe

logger = logging.getLogger(__name__)


class NotNodeFoundError(Exception):
    pass

class ProvideMutation(BaseMutation):
    Output = ProvisionType

    class Arguments:
        node = graphene.ID(required=True, description="The node's id")
        reference = graphene.String(required=False, description="This Pods unique Reference (for the Client)")
        parent = graphene.String(required=False, description="The parent provision")
        selector = SelectorInput(required=True, description="The Selector")

    @classmethod
    def change(cls, context, root, info, *arg, **kwargs):
        logger.info("Publishing it to the Consumer")

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        nodeid = kwargs.pop("node") if "node" in kwargs else None
        parent = kwargs.pop("parent") if "parent" in kwargs else None
        selector = kwargs.pop("selector") if "selector" in kwargs else "__auto__"

        try:
            node = Node.objects.get(id=nodeid)
        except:
            raise NotNodeFoundError("Please specifiy a correct NodeID")
        
        provision = provision_pod_pipe(context, reference, node, selector, parent)

        return provision
