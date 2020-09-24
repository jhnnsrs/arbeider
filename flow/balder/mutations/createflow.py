import graphene
from graphene.types.generic import GenericScalar

from balder.mutations.base import BaseMutation
from flow.models import Graph
from flow.balder.types import GraphType

class CreateFlowMutation(BaseMutation):
    status = graphene.String()
    graph = graphene.Field(GraphType, description="The Graph")

    class Arguments:
        name = graphene.String(required=True, description ="The name for this flow")
        diagram = GenericScalar(description="The diagram")
        version = graphene.String(description="The version of this", required=False)
        description = graphene.String(description="The description of this Flow", required=False)

    @staticmethod
    def mutate(root, info, **kwargs):
        diagram = kwargs.get("diagram")
        print(diagram["id"])
        name = kwargs.get("name")
        version = kwargs.get("version", "1.0")
        description = kwargs.get("description", "Not Set")
        user = info.context.user
        #TODO: implement check for permisions
        if not user.is_authenticated: raise Exception("You must be logged in to do this")


        graph, status = Graph.objects.get_or_create(
            diagram = diagram,
            creator = user,
            version = version,
            name = name,
            description = description
        )
        

        
        return CreateFlowMutation(status=status, graph=graph)