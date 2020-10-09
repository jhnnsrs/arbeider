from flow.balder.types import PortInputType
import graphene
from graphene.types.generic import GenericScalar

from balder.mutations.base import BaseMutation
from flow.models import Flow
from delt.models import Node, Repository
from balder.delt.models import NodeType







def get_flow_repository_for_id(user, id="localhost"):
    repo, _ = Repository.objects.filter(creator=user).get_or_create(name=f"flow_{id}")
    return repo

class CreateNodeMutation(BaseMutation):
    Output = NodeType

    class Arguments:
        description = graphene.String(required=True, description="A description for the Node")
        name = graphene.String(description="The name of this template", required=False)
        outputs = graphene.List(PortInputType, description="The Outputs")
        inputs = graphene.List(PortInputType, description="The Inputs")
        variety = graphene.String(description="The variety")
        interface = graphene.String(description="The Interface")
        package = graphene.String(description="The Package")


    @staticmethod
    def change(context, *args,  **kwargs):
        user = context.user
        #TODO: Check permissions

        name = kwargs.get("name")
        description = kwargs.get("description", "No Description")
        variety = kwargs.get("variety", "flow")
        outputs = kwargs.get("outputs", [])
        inputs = kwargs.get("inputs", [])
        realm = "flow_localhost"
        interface = kwargs.get("name", "oinoisnoein")
        package = kwargs.get("package", "flow_localhost")
        repository = get_flow_repository_for_id(user)

        description = kwargs.get("description", "Not Set")

        node = Node(
            name=name,
            description = description,
            inputs=inputs,
            outputs=outputs,
            variety=variety,
            realm=realm,
            interface=interface,
            package=package,
            repository=repository
        )

        node.save()

    
        return node