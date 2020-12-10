from flow.mutations.compile import CompileMutation
from flow.types import CompilerType, ExecutionGraphType
from flow.balder.mutations.createnode import CreateNodeMutation
import graphene

from balder.register import register_mutation, register_query
from balder.wrappers import BalderMutationWrapper, BalderObjectWrapper
from flow.balder.mutations.createflow import CreateFlowMutation
from flow.models import Compiler, ExecutionGraph, Flow, FlowNode, Graph
from flow.balder.types import FlowNodeType, FlowType, GraphType


@register_mutation("createNode", description="Create a graph from a diagram")
class CreateNode(BalderMutationWrapper):
    mutation = CreateNodeMutation


@register_mutation("createFlow", description="Create a Flow from a diagram")
class CreateFlow(BalderMutationWrapper):
    mutation = CreateFlowMutation


@register_mutation("compile", description="Takes a Graph and compiles it with the help of a Compiler")
class Compile(BalderMutationWrapper):
    mutation = CompileMutation


@register_query("graph", 
    description="Get the graph", 
    id=graphene.ID(required=True, description="the Graph id")
)
class GraphItemWrapper(BalderObjectWrapper):
    object_type = GraphType
    resolver = lambda context, id: Graph.objects.get(id=id)
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
class FlowDetail(BalderObjectWrapper):
    object_type = FlowNodeType
    resolver = lambda context, id: FlowNode.objects.get(id=id)
    asfield = True


@register_query("compilers", 
    description="Get the Compilers",
)
class CompilerList(BalderObjectWrapper):
    object_type = CompilerType
    resolver = lambda context: Compiler.objects.all()
    aslist = True

@register_query("executiongraphs", 
    description="Get the Exceqution Graph",
)
class ExcequtionGraphList(BalderObjectWrapper):
    object_type = ExecutionGraphType
    resolver = lambda context: ExecutionGraph.objects.all()
    aslist = True
