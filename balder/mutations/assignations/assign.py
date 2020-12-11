import logging
import uuid

import graphene
from graphene.types.generic import GenericScalar

from balder.delt.models import AssignationType
from balder.mutations.base import BaseMutation
from delt.models import Node, Pod, Provision
from delt.pipes import assign_inputs_pipe

logger = logging.getLogger(__name__)


class NoPodFoundError(Exception):
    pass

class AssignMutation(BaseMutation):
    Output = AssignationType

    class Arguments:
        pod = graphene.ID(required=True, description="The pod's id")
        inputs = GenericScalar(required=True, description="The Inputs")
        reference = graphene.String(required=False, description="This jobs reference")

    @classmethod
    def change(cls, context, root, info, *arg, **kwargs):

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        podid = kwargs.pop("pod") if "pod" in kwargs else None
        inputs = kwargs.pop("inputs") if "inputs" in kwargs else None

        try:
            pod = Pod.objects.get(id=podid)
        except:
            raise NoPodFoundError("Please specifiy a correct NodeID")
        
        assignation = assign_inputs_pipe(context, reference, pod, inputs)
        logger.error(f"Sending Assignation {str(assignation)}")
        return assignation
