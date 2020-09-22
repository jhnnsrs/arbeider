from balder.delt.types import BoolPortType, FilePortType, ListPortType, PortType, CharPortType, IntPortType, ModelPortType, ObjectPortType, UUIDPortType
import channels_graphql_ws
import graphene
from graphene import Dynamic
from graphene.types import generic

from balder.discover import autodiscover_balder
from balder.registry import get_registry
from delt.models import Job





rootquery = None
rootsubscription = None
rootmutation = None


def buildRootMutation():
    global rootmutation
    if rootmutation is None:
        fields  = get_registry().getMutationFields()
        rootmutation = type('Mutation', (graphene.ObjectType,), { **fields, "__doc__": "All Mutations are to be found here"})
    return rootmutation


def buildRootSubscription():
    global rootsubscription
    if rootsubscription is None:
        fields  = get_registry().getSubscriptionFields()
        rootsubscription = type('Subscription', (graphene.ObjectType,), { **fields, "__doc__": "All Subscriptions are to be found here"})
    return rootsubscription



def buildRootQuery():
    global rootquery
    if rootquery is None:
        fields  = get_registry().getQueryFields()
        rootquery = type('Query', (graphene.ObjectType,), { **fields, "__doc__": "This is the Root Query"})
    return rootquery


# We will Autodiscover everything in the Default Space
autodiscover_balder("default")

class Mutation(graphene.ObjectType):
    """Root GraphQL mutation."""
    # Check Graphene docs to see how to define mutations.
    pass


graphql_schema = graphene.Schema(
    query=buildRootQuery(),
    subscription=buildRootSubscription(),
    mutation=buildRootMutation(),
    types= [PortType, IntPortType, ModelPortType, ObjectPortType, IntPortType, CharPortType, UUIDPortType, BoolPortType, ListPortType, FilePortType]
)