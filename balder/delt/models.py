from balder.delt.ports import PortType
import graphene
from balder.types import BalderObjectType
from delt.models import *


class RepositoryType(BalderObjectType):

    class Meta:
        model = Repository

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


class AssignationType(BalderObjectType):

    class Meta:
        model = Assignation

class ProvisionType(BalderObjectType):

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
