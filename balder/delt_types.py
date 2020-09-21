from guardian.compat import get_user_model

from balder.types import BalderObjectType
from balder.delt.types import PortType
from delt.models import Job, Node, Pod, Route, Provision, Assignation
import graphene

from graphene_django.converter import convert_django_field

from balder.fields import Inputs, Outputs, Image
from delt.fields import InputsField, OutputsField
from django.db.models import ImageField

@convert_django_field.register(ImageField)
def convert_field_to_string(field, registry=None):
    return Image(field, description=field.help_text, required=not field.null)


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
