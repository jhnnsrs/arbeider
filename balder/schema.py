from delt.nodes.base import NODE_BACKEND_SETTINGS_FIELD
import graphene
from graphene.types import generic
from django.db import models
from balder.discover import autodiscover_balder
from balder.registry import get_balder_registry
from balder.delt.ports import *
from balder import fields
from balder.delt.enums import *
from graphene_django.converter import convert_django_field
from delt.fields import InputsField, OutputsField
# This File Gets called upon Schema Creation
rootquery = None
rootsubscription = None
rootmutation = None
roottypes = None


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
    roottypes += [SliderWidgetType, ObjectWidgetType, SwitchWidgetType, CharWidgetType, ModelWidgetType, IntWidgetType, UUIDWidgetType, FileWidgetType, ListWidgetType, QueryWidgetType, SliderQueryWidgetType, FakeWidgetType]
    roottypes += [PodStatusEnum, AssignationStatusEnum, EndpointEnum, ClientTypeEnum]
    return roottypes


# We will Autodiscover everything in the Default Space
autodiscover_balder("default")


graphql_schema = graphene.Schema(
    query=buildRootQuery(),
    subscription=buildRootSubscription(),
    mutation=buildRootMutation(),
    types= buildRootTypes()
)