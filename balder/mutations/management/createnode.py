from delt.integrity import node_identifier
from delt.constants.scopes import CAN_ADD_NODES
from balder.delt.inputs import PortInputType
import graphene


from delt.bouncers.context import BouncerContext
from balder.mutations.base import BaseMutation
from delt.models import Node, Repository
from balder.delt.models import NodeType


def get_node_repository(user, id="localhost"):
    repo, _ = Repository.objects.filter(creator=user).get_or_create(type=f"flow", defaults={"name": f"flow_{id}", "creator": user})
    return repo

class CreateNodeMutation(BaseMutation):
    Output = NodeType

    class Arguments:
        description = graphene.String(required=True, description="A description for the Node")
        name = graphene.String(description="The name of this template", required=True)
        outputs = graphene.List(PortInputType, description="The Outputs")
        inputs = graphene.List(PortInputType, description="The Inputs")
        variety = graphene.String(description="The variety")
        interface = graphene.String(description="The Interface", required=True)
        package = graphene.String(description="The Package", required=True)


    @staticmethod
    def change(context: BouncerContext, *args,  **kwargs):
        if not context.can(CAN_ADD_NODES): raise Exception("User is not authorized to add Nodes")

        
        user = context.user
        repository = get_node_repository(user)
        package = kwargs.get("package")
        interface = kwargs.get("interface")

        description = kwargs.get("description", "Not Set")

        identifier = node_identifier(package=package, interface=interface)
        
        node, created = Node.objects.get_or_create(identifier=identifier, defaults={**kwargs, "repository": repository})
   
        return node