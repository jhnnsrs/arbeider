from balder.types import BalderObjectType
from balder.delt_types import NodeType
from flow.models import Graph, FlowNode

class GraphType(BalderObjectType):
    """ A Graph is a representation of diagram and can generate a flow """
    class Meta:
        model = Graph
        description = Graph.__doc__


class FlowNodeType(NodeType):
    """ A Graph is a representation of diagram and can generate a flow """
    class Meta:
        model = FlowNode
        description = FlowNode.__doc__

