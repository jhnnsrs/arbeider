from graphene.types.generic import GenericScalar
from graphene.types.inputobjecttype import InputObjectType

from balder.delt.models import NodeType
from balder.types import BalderObjectType
from flow.models import FlowNode, Graph, Flow
import graphene


class WidgetInputType(InputObjectType):
    type = graphene.String(description="type", required=True)
    query = graphene.String(description="Do we have a possible")





class PortInputType(InputObjectType):
    key=  graphene.String(description="The Key", required=True)
    type = graphene.String(description="the type of input", required=True)
    description = graphene.String(description="A description for this Port", required= False)
    required= graphene.Boolean(description="Is this field required", required=True)
    label = graphene.String(description="The Label of this inport")
    dependencies = graphene.List(graphene.String, description="The dependencies of this port")
    default = GenericScalar(description="Does this field have a specific value")
    identifier= graphene.String(description="The corresponding Model")
    widget = graphene.Field(WidgetInputType, description="Which Widget to use to render Port in User Interfaces")



class GraphType(BalderObjectType):
    """ A Graph is a representation of diagram and can generate a flow """
    diagram = GenericScalar()



    class Meta:
        model = Graph
        description = Graph.__doc__


class FlowNodeType(NodeType):
    """ A Graph is a representation of diagram and can generate a flow """
    class Meta:
        model = FlowNode
        description = FlowNode.__doc__
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }

class FlowType(BalderObjectType):

    """ A Flow is a representation of diagram and can generate a flow """
    class Meta:
        model = Flow
        description = Flow.__doc__
