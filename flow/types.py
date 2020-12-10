import graphene
from balder.types import BalderObjectType
from flow.models import Graph, ExecutionGraph, Compiler, CompilerRoute


class CompilerType(BalderObjectType):
    class Meta:
        model = Compiler

class GraphType(BalderObjectType):

    class Meta:
        model = Graph


class ExecutionGraphType(BalderObjectType):

    class Meta:
        model = ExecutionGraph


class CompilerRouteType(BalderObjectType):

    class Meta:
        model = CompilerRoute