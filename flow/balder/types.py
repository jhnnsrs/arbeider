from graphene.types.generic import GenericScalar

from balder.delt_types import NodeType
from balder.types import BalderObjectType
from flow.models import FlowNode, Graph


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
