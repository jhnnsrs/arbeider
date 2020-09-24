from delt.orchestrator import get_orchestrator
import graphene
from graphene.types.generic import GenericScalar

from balder.mutations.base import BaseMutation


class SlotMutation(BaseMutation):
    status = graphene.String()

    class Arguments:
        gate = graphene.String(required=True, description ="The Unique id for the gate")
        job = graphene.String(required=True, description ="The Unique id for the job")
        outputs = GenericScalar(description="The Outputs for this Node")

    @staticmethod
    def mutate(root, info, **kwargs):
        get_orchestrator().getHandlerForProvider("fremmed").on("slot_in")(**kwargs)