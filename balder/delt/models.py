import avatar
from django_filters import filterset
from balder.delt.ports import PortType
import graphene
from balder.types import BalderObjectType
from delt.models import *
from avatar.models import Avatar
from balder import fields
from django.db import models
from django_filters import FilterSet
from graphene_django.converter import convert_django_field
from delt.fields import InputsField, OutputsField

# TODO: find a better place to register these fields... they need to be imported before the models are imported

@convert_django_field.register(OutputsField)
def convert_json_field_to_string(field, registry=None):
    return fields.Inputs()

@convert_django_field.register(InputsField)
def convert_json_field_to_string(field, registry=None):
    return fields.Outputs()


@convert_django_field.register(models.ImageField)
def convert_field_to_string(field, registry=None):
    return fields.ImageField(field, description=field.help_text, required=not field.null)


class AvatarType(BalderObjectType):

    class Meta:
        model = Avatar


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

class ProviderType(BalderObjectType):

    class Meta:
        model = Provider


class DataPointsType(BalderObjectType):

    class Meta:
        model = DataPoint


class DataModelType(BalderObjectType):
    extenders = graphene.List(graphene.String, description="The extenders")

    class Meta:
        model = DataModel



class SelectorType(BalderObjectType):

    class Meta:
        model = Selector


class TemplateType(BalderObjectType):

    class Meta:
        model = Template

class UserType(BalderObjectType):
    avatar = graphene.Field(AvatarType)

    class Meta:
        model = get_user_model()
        exclude = ("password",)

    def resolve_avatar(parent, info):
        try:
            return Avatar.objects.get(user=parent,primary=True)
        except:
            return None