from flow.utils import validate_flow
import graphene
from graphene.types.generic import GenericScalar


from delt.bouncers.context import BouncerContext
from balder.mutations.base import BaseMutation
from flow.models import Engine, Flow
from delt.models import Node
from flow.balder.types import FlowType




class CreateFlowMutation(BaseMutation):
    Output = FlowType

    class Arguments:
        node = graphene.ID(required=True, description ="The id for the node of this Flow")
        diagram = GenericScalar(description="The diagram")
        version = graphene.String(description="The version of this", required=False)
        engine = graphene.String(description="The engine", required=True)

    @classmethod
    def change(cls, context, *args, **kwargs):
        diagram = kwargs.get("diagram")
        node_id = kwargs.get("node")
        version = kwargs.get("version")
        engine = kwargs.get("engine")
        user = context.user


        #TODO: implement check for permisions
        if not user.is_authenticated: raise Exception("You must be logged in to do this")

        node = Node.objects.get(id=node_id)
        if (validate_flow(diagram=diagram)):
            flow = Flow.objects.create(
                diagram = diagram,
                creator = user,
                version = version,
                node = node,
                engine = Engine.objects.get(name=engine)
            )
        else:
            raise Exception("Not a valid Diagram")
    
        return flow