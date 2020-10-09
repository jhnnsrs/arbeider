from flow.utils import validate_flow
import graphene
from graphene.types.generic import GenericScalar

from balder.mutations.base import BaseMutation
from flow.models import Flow
from delt.models import Node
from flow.balder.types import FlowType

class CreateFlowMutation(BaseMutation):
    Output = FlowType

    class Arguments:
        node = graphene.ID(required=True, description ="The id for the node of this Flow")
        diagram = GenericScalar(description="The diagram")
        name = graphene.String(description="The name of this template", required=False)

    @staticmethod
    def change(root, context, **kwargs):
        diagram = kwargs.get("diagram")
        name = kwargs.get("name")
        node_id = kwargs.get("node")
        description = kwargs.get("description", "Not Set")
        user = context.user
        #TODO: implement check for permisions
        if not user.is_authenticated: raise Exception("You must be logged in to do this")

        node = Node.objects.get(id=node_id)
        if (validate_flow(diagram=diagram)):
            flow = Flow.objects.create(
                diagram = diagram,
                creator = user,
                name = name,
                node = node
            )
        else:
            raise Exception("Not a valid Diagram")
    
        return flow