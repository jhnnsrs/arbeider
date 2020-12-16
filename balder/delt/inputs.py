import graphene
from graphene.types.generic import GenericScalar

class SelectorInput(graphene.InputObjectType):
    provider = graphene.String(required=True, description="The provider you want to select")
    kwargs = GenericScalar(required=True, description="The kwargs for the provider")




class WidgetInputType(graphene.InputObjectType):
    type = graphene.String(description="type", required=True)
    query = graphene.String(description="Do we have a possible")


class PortInputType(graphene.InputObjectType):
    key=  graphene.String(description="The Key", required=True)
    type = graphene.String(description="the type of input", required=True)
    description = graphene.String(description="A description for this Port", required= False)
    required= graphene.Boolean(description="Is this field required", required=True)
    primary = graphene.Boolean(description="Is this a primary port", required=False)
    label = graphene.String(description="The Label of this inport")
    dependencies = graphene.List(graphene.String, description="The dependencies of this port")
    default = GenericScalar(description="Does this field have a specific value")
    identifier= graphene.String(description="The corresponding Model")
    widget = graphene.Field(WidgetInputType, description="Which Widget to use to render Port in User Interfaces")