import graphene
from graphene.types.generic import GenericScalar

class SelectorInput(graphene.InputObjectType):
    provider = graphene.String(required=True, description="The provider you want to select")
    kwargs = GenericScalar(required=True, description="The kwargs for the provider")