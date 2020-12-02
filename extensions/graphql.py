from balder.mutations.negotiations.negotiate import NegotiateMutation
from extensions.filters import NodeListFilter
from graphene.types.generic import GenericScalar
from balder.subscriptions.assignation.watch import WatchSubscription
from balder.subscriptions.helpers.myprovisions import MyProvisionsSubscription, MyProvisions
from balder.delt.ports import get_port_types, get_widget_types
from delt.bouncers.context import BouncerContext
import graphene

from balder.delt.models import AssignationType, NodeType, PodType, ProvisionType, UserType
from balder.mutations.assignations.assign import AssignMutation
from balder.mutations.provisions.provide import ProvideMutation
from balder.register import (register_mutation, register_query,
                             register_subscription)
from balder.subscriptions.provisions.monitor import MonitorSubscription
from balder.subscriptions.assignation.assign import AssignSubscription
from balder.subscriptions.provisions.provide import ProvideSubscription
from balder.wrappers import (BalderMutationWrapper, BalderObjectWrapper, BalderSubscriptionWrapper)
from delt.models import Assignation, Node, Pod, Provision
from extensions.fremmed.mutations import SlotMutation
from extensions.fremmed.subscriptions import GateSubscription


@register_mutation("negotiate", description="Negotiate our protocols")
class Negotiate(BalderMutationWrapper):
    mutation = NegotiateMutation




@register_query("nodes", description="Get all nodes in this bergen instance", withfilter=NodeListFilter)
class NodeListWrapper(BalderObjectWrapper):
    object_type = NodeType
    resolver = lambda root, info: Node.objects.all()
    aslist = True


class ListItem(graphene.ObjectType):
    key = graphene.String()
    label = graphene.String()
    description= graphene.String()
    value = GenericScalar()



@register_query("porttypes", description="Get all PortTypes in this bergen instance")
class PortTypesListWrapper(BalderObjectWrapper):
    object_type = ListItem
    resolver = lambda root, info: map(lambda item: { "key": item[0], "label": item[1].__name__, "description": item[1].__doc__}, list(get_port_types().items()))
    aslist = True

@register_query("widgettypes", description="Get all WidgetTypes in this bergen instance")
class WidgetTypesWrapper(BalderObjectWrapper):
    object_type = ListItem
    resolver = lambda root, info: map(lambda item: { "key":  item[0], "label": item[1].__name__, "description": item[1].__doc__}, list(get_widget_types().items()))
    aslist = True

@register_query("pod", description="Get all nodes in this bergen instance", id = graphene.ID(description="The Pods ID"))
class NodeListWrapper(BalderObjectWrapper):
    object_type = PodType
    resolver = lambda root, context, id: Pod.objects.get(id=id)
    asfield = True

@register_query("latestnodes", description="Get your recently used nodes")
class NodeListWrapper(BalderObjectWrapper):
    object_type = NodeType
    aslist = True

    @staticmethod
    def resolver(root, context):
        #TODO: Implement the proper 
        return Node.objects.exclude(variety="output").exclude(variety="input")[:10]


@register_query("podsformodel", models= graphene.List(graphene.String, description="The pods models (assignable)"), description="Gets all running pods for the Model")
class NodeWrapper(BalderObjectWrapper):
    object_type = PodType
    aslist = True

    def resolve(context, models):
        #TODO: Implement check before this
        pods = Pod.objects.accessible(context.user)
        for model in models:
            pods = pods.filter(node__inputs__contains=[{"identifier": model}])

        return pods



@register_query("node", id= graphene.ID(description="The node's ID"), description="Get a nodes in this bergen instance")
class NodeWrapper(BalderObjectWrapper):
    object_type = NodeType
    asfield = True
    resolve = lambda context, id: Node.objects.get(id=id)


@register_query("monitor", reference= graphene.String(description="The monitored Provision"), description="Show the status of a NOde")
class MonitorQueryWrapper(BalderObjectWrapper):
    object_type = ProvisionType
    asfield = True
    resolve = lambda context, reference: Provision.objects.get(reference=reference)



@register_mutation("slot", description="Input for a Node")
class Slot(BalderMutationWrapper):
    mutation = SlotMutation


@register_query("me", description="Show the currently logged in user")
class MeQueryWrapper(BalderObjectWrapper):
    object_type = UserType
    asfield = True
    resolve = lambda context: context.user

@register_query("myprovisions", description="Show the currently provisions for the user")
class MeQueryWrapper(BalderObjectWrapper):
    object_type = ProvisionType
    aslist = True
    resolve = lambda context: MyProvisions(context.user)


@register_subscription("myprovisions", description="Show Provisions for the currently logged in users")
class MyProvisionSubscriptionWrapper(BalderSubscriptionWrapper):
    ''' This provides a fast way to provide a node though a provision and moniters it on the way, violates CQRS patterns'''
    subscription = MyProvisionsSubscription
    

#    _____  _____   ______      _______  _____ _____ ____  _   _ 
#   |  __ \|  __ \ / __ \ \    / /_   _|/ ____|_   _/ __ \| \ | |
#   | |__) | |__) | |  | \ \  / /  | | | (___   | || |  | |  \| |
#   |  ___/|  _  /| |  | |\ \/ /   | |  \___ \  | || |  | | . ` |
#   | |    | | \ \| |__| | \  /   _| |_ ____) |_| || |__| | |\  |
#   |_|    |_|  \_\\____/   \/   |_____|_____/|_____\____/|_| \_|
#                                                                
#  Provision Related Mutation

@register_mutation("provide", description="Provision Pod")
class ProvideMutationWrapper(BalderMutationWrapper):
    mutation = ProvideMutation

@register_query("monitor", reference= graphene.String(description="The monitored Provision"), description="Show the status of a Provision")
class MonitorQueryWrapper(BalderObjectWrapper):
    object_type = ProvisionType
    asfield = True

    @staticmethod
    def resolver(root, info, reference):
        return Provision.objects.get(reference=reference)

@register_subscription("provide", description="Provision Pods for Nodes (in one go)")
class ProvideSubscriptionWrapper(BalderSubscriptionWrapper):
    ''' This provides a fast way to provide a node though a provision and moniters it on the way, violates CQRS patterns'''
    subscription = ProvideSubscription

@register_subscription("monitor", description="Monitor a Provision for changes")
class MonitorSubscriptionWrapper(BalderSubscriptionWrapper):
    ''' This provides a fast way to provide a node though a provision and moniters it on the way, violates CQRS patterns'''
    subscription = MonitorSubscription


@register_subscription("gate", description="Gate Way")
class Gate(BalderSubscriptionWrapper):
    subscription = GateSubscription



# ASSIGNATION SHIT



@register_mutation("assign", description="Assign Job")
class AssignMutationWrapper(BalderMutationWrapper):
    mutation = AssignMutation

@register_subscription("assign", description="Assign Jobs for a Pod (in one go)")
class AssignSubscriptionWrapper(BalderSubscriptionWrapper):
    ''' This provides a fast way to provide a node though a provision and moniters it on the way, violates CQRS patterns'''
    subscription = AssignSubscription

@register_query("watch", reference= graphene.String(description="The monitored assignation"), description="Show the status of a Assignation")
class MonitorQueryWrapper(BalderObjectWrapper):
    object_type = AssignationType
    asfield = True

    @staticmethod
    def resolver(root, info, reference):
        return Assignation.objects.get(reference=reference)

@register_subscription("watch", description="Monitor a Job for changes")
class MonitorSubscriptionWrapper(BalderSubscriptionWrapper):
    ''' The Proper way to watch for changes in an assignation'''
    subscription = WatchSubscription