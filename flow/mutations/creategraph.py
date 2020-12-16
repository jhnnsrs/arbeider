from flow.types import GraphType
from flow.utils import validate_graph
import graphene
from graphene.types.generic import GenericScalar
from delt.bouncers.context import BouncerContext
from balder.mutations.base import BaseMutation
from flow.models import  Graph
from delt.models import Node

class CreateGraphMutation(BaseMutation):
    Output = GraphType

    class Arguments:
        node = graphene.ID(required=True, description ="The id for the node of this Flow")
        diagram = GenericScalar(description="The diagram")
        version = graphene.String(description="The version of this", required=False)
    
    @classmethod
    def change(cls, context, *args, **kwargs):
        diagram = kwargs.get("diagram")
        node_id = kwargs.get("node")
        version = kwargs.get("version")
        user = context.user





        #TODO: implement check for permisions
        if not user.is_authenticated: raise Exception("You must be logged in to do this")

        node = Node.objects.get(id=node_id)
        if (validate_graph(diagram=diagram)):
            flow = Graph.objects.create(
                diagram = diagram,
                creator = user,
                version = version,
                node = node
            )
        else:
            raise Exception("Not a valid Diagram")
    
        return flow