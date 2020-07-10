from guardian.compat import get_user_model

from balder.types import BalderObjectType
from balder.delt.types import PortType
from delt.models import Job, Node, Pod, Route, Provision
import graphene

class PodType(BalderObjectType):

    class Meta:
        model = Pod

class NodeType(BalderObjectType):
    outputs = graphene.List(PortType)
    inputs = graphene.List(PortType)

    class Meta:
        model = Node
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }


class ProvisionType(BalderObjectType):
    children = graphene.List(lambda: ProvisionType)

    class Meta:
        model = Provision

class RouteType(BalderObjectType):

    class Meta:
        model = Route
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }

class JobType(BalderObjectType):

    class Meta:
        model = Job

class UserType(BalderObjectType):

    class Meta:
        model = get_user_model()
        exclude = ("password",)
