from balder.fields import ImageField
from delt.nodes.base import NODE_BACKEND_SETTINGS_FIELD
import channels_graphql_ws
import graphene
from graphene import Dynamic
from graphene.types import generic
from django.db import models
from balder.discover import autodiscover_balder
from balder.registry import get_balder_registry
from delt.models import Job
from balder.delt.ports import *
from balder import fields

from graphene_django.converter import convert_django_field
from delt.fields import InputsField, OutputsField
# This File Gets called upon Schema Creation
rootquery = None
rootsubscription = None
rootmutation = None
roottypes = None

@convert_django_field.register(OutputsField)
def convert_json_field_to_string(field, registry=None):
    return fields.Inputs()

@convert_django_field.register(InputsField)
def convert_json_field_to_string(field, registry=None):
    return fields.Outputs()


@convert_django_field.register(models.ImageField)
def convert_field_to_string(field, registry=None):
    return fields.ImageField(field, description=field.help_text, required=not field.null)



def buildRootMutation():
    global rootmutation
    if rootmutation is None:
        fields  = get_balder_registry().getMutationFields()
        rootmutation = type('Mutation', (graphene.ObjectType,), { **fields, "__doc__": "All Mutations are to be found here"})
    return rootmutation


def buildRootSubscription():
    global rootsubscription
    if rootsubscription is None:
        fields  = get_balder_registry().getSubscriptionFields()
        rootsubscription = type('Subscription', (graphene.ObjectType,), { **fields, "__doc__": "All Subscriptions are to be found here"})
    return rootsubscription



def buildRootQuery():
    global rootquery
    if rootquery is None:
        fields  = get_balder_registry().getQueryFields()
        rootquery = type('Query', (graphene.ObjectType,), { **fields, "__doc__": "This is the Root Query"})
    return rootquery


def buildRootTypes():
    global roottypes
    if roottypes is None:
        fields  = get_balder_registry().getTypeFields()
        roottypes = [value for key, value in fields.items()]

    roottypes += [PortType, IntPortType, ModelPortType, ObjectPortType, IntPortType, CharPortType, UUIDPortType, BoolPortType, ListPortType, FilePortType]
    return roottypes


# We will Autodiscover everything in the Default Space
autodiscover_balder("default")


graphql_schema = graphene.Schema(
    query=buildRootQuery(),
    subscription=buildRootSubscription(),
    mutation=buildRootMutation(),
    types= buildRootTypes()
)