from flow.mutations.updategraph import UpdateGraphMutation
from flow.mutations.compile import CompileMutation
from flow.types import CompilerType, ExecutionGraphType
import graphene

from balder.register import register_mutation, register_query
from balder.wrappers import BalderMutationWrapper, BalderObjectWrapper
from flow.models import Compiler, ExecutionGraph, Graph
from flow.types import GraphType
from flow.mutations.creategraph import CreateGraphMutation


@register_mutation("createGraph", description="Create a Flow from a diagram")
class CreateGraph(BalderMutationWrapper):
    mutation = CreateGraphMutation

@register_mutation("updateGraph", description="Create a Flow from a diagram")
class UpdateGraphh(BalderMutationWrapper):
    mutation = UpdateGraphMutation


@register_mutation("compile", description="Takes a Graph and compiles it with the help of a Compiler")
class Compile(BalderMutationWrapper):
    mutation = CompileMutation


@register_query("graph", 
    description="Get the graph", 
    id=graphene.ID(required=True, description="the Graph id")
)
class GraphItemWrapper(BalderObjectWrapper):
    object_type = GraphType
    resolve = lambda context, id: Graph.objects.get(id=id)
    asfield = True


@register_query("mygraphs", 
    description="Get your graphs", 
)
class MyGraphsWrapper(BalderObjectWrapper):
    object_type = GraphType
    resolve = lambda context, id: Graph.objects.filter(creator=context.user)
    aslist = True

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
