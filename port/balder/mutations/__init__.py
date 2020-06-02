import graphene
from graphene.types.generic import GenericScalar

from balder.mutations.base import BaseMutation
from delt.settingsregistry import get_settings_registry


class CreateFlowMutation(BaseMutation):
    status = graphene.String()

    class Arguments:
        name = graphene.String(required=True, description ="The name for this flow")
        diagram = GenericScalar(description="The diagram")

    @staticmethod
    def mutate(root, info, **kwargs):
        return CreateFlowMutation(status="created")

