from balder.delt.models import NodeType
from delt.models import Node
from flow.balder.mutations.createnode import CreateNodeMutation
import graphene

from balder.register import register_mutation, register_query
from balder.wrappers import BalderMutationWrapper, BalderObjectWrapper
from flow.balder.mutations.createflow import CreateFlowMutation
from flow.balder.mutations.toflow import ToFlowMutation
from flow.models import Flow, FlowNode, Graph
from flow.balder.types import FlowNodeType, FlowType, GraphType


@register_mutation("createNode", description="Create a graph from a diagram")
class CreateNode(BalderMutationWrapper):
    mutation = CreateNodeMutation


@register_mutation("createFlow", description="Create a Flow from a diagram")
class CreateFlow(BalderMutationWrapper):
    mutation = CreateFlowMutation


@register_mutation("toFlow", description="Takes a Graph and creates or updates a Flow out of it")
class ToFlow(BalderMutationWrapper):
    mutation = ToFlowMutation


@register_query("graph", 
    description="Get the graph", 
    id=graphene.ID(required=True, description="the Graph id")
)
class GraphItemWrapper(BalderObjectWrapper):
    object_type = GraphType
    resolver = lambda root, info, id: Graph.objects.get(id=id)
    asfield = True


@register_query("myflows", 
    description="Get all Flows", 
)
class FlowsWrapper(BalderObjectWrapper):
    object_type = FlowType
    resolve = lambda context: Flow.objects.filter(node__repository__type="flow", node__repository__creator=context.user)
    aslist = True

@register_query("flow", 
    description="Get the flow", 
    id=graphene.ID(required=True, description="the Flow id")
)
class GraphItemWrapper(BalderObjectWrapper):
    object_type = FlowNodeType
    resolver = lambda root, info, id: FlowNode.objects.get(id=id)
    asfield = True
