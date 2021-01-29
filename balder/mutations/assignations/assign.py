from balder.scalars.models import NodeID
import logging
import uuid

import graphene
from graphene.types.generic import GenericScalar

from balder.delt.models import AssignationType
from balder.mutations.base import BaseMutation
from delt.models import Node, Pod, Provision
from delt.pipes import assign_inputs_pipe, assign_inputs_to_node_pipe

logger = logging.getLogger(__name__)


class NoPodFoundError(Exception):
    pass

class AssignMutation(BaseMutation):
    Output = AssignationType

    class Arguments:
        node = NodeID(required=False, description="The node id")
        pod = graphene.ID(required=False, description="The pod id")
        template = graphene.ID(required=False, description="The template id")
        reference = graphene.String(required=True, description="The pods id")
        inputs = GenericScalar(required=True, description="The Inputs for this Pod")

    @classmethod
    def change(cls, context, root, info, *arg, **kwargs):

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        inputs = kwargs.pop("inputs") if "inputs" in kwargs else None
        podid = kwargs.pop("pod") if "pod" in kwargs else None
        node = kwargs.pop("node") if "node" in kwargs else None
        templateid = kwargs.get("template", None)

        if node:
            print(node)
            assignation = assign_inputs_to_node_pipe(context, reference, inputs, node)
            return assignation

        if podid:
            try:
                pod = Pod.objects.get(id=podid)
            except Pod.DoesNotExist:
                raise Exception("The pod you specified does not exist!")
        
