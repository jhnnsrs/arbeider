from flow.types import GraphType
from flow.utils import validate_graph
import graphene
from graphene.types.generic import GenericScalar
from delt.bouncers.context import BouncerContext
from balder.mutations.base import BaseMutation
from flow.models import  Graph
from delt.models import Node

class UpdateGraphMutation(BaseMutation):
    Output = GraphType

    class Arguments:
        graph = graphene.ID(required=True, description ="The id for the graph of this Flow")
        diagram = GenericScalar(description="The diagram")


    @classmethod
    def change(cls, context, *args, **kwargs):
        diagram = kwargs.get("diagram")
        graph = kwargs.get("graph")
        user = context.user

        #TODO: implement check for permisions
        if not user.is_authenticated: raise Exception("You must be logged in to do this")

        graph = Graph.objects.get(id=graph)
        if (validate_graph(diagram=diagram)):
            graph.diagram = diagram
            graph.save()
        else:
            raise Exception("Not a valid Diagram")
    
        return graph