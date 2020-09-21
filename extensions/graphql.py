from balder.subscriptions.helpers.myprovisions import MyProvisionsSubscription, MyProvisions
from delt.bouncers.context import BouncerContext
import graphene
from django.forms.models import model_to_dict
from graphene.types.generic import GenericScalar

from balder.delt_types import JobType, NodeType, PodType, ProvisionType, UserType
from balder.mutations.assignations.assign import AssignMutation
from balder.mutations.provisions.provide import ProvideMutation
from balder.queries.provisions.monitor import MonitorQuery
from balder.register import (register_mutation, register_query,
                             register_subscription)
from balder.subscriptions.provisions.monitor import MonitorSubscription
from balder.subscriptions.jobs.assign import AssignSubscription
from balder.subscriptions.jobs.check import CheckSubscription
from balder.subscriptions.provisions.provide import ProvideSubscription
from balder.wrappers import (BalderMutationWrapper, BalderObjectWrapper,
                             BalderQueryWrapper, BalderSubscriptionWrapper)
from delt.models import Job, Node, Pod, Provision
from delt.shortcuts import get_pod_for_selector
from extensions.fremmed.mutations import SlotMutation
from extensions.fremmed.subscriptions import GateSubscription
from extensions.types.fremmed import FrontendPodType
from fremmed.models import FrontendPod
from fremmed.serializers import FrontendPodSerializer


@register_query("nodes", description="Get all nodes in this bergen instance", withfilter=True)
class NodeListWrapper(BalderObjectWrapper):
    object_type = NodeType
    resolver = lambda root, info: Node.objects.all()
    aslist = True


@register_query("latestnodes", description="Get your recently used nodes")
class NodeListWrapper(BalderObjectWrapper):
    object_type = NodeType
    aslist = True

    @staticmethod
    def resolver(root, context):
        #TODO: Implement the proper 
        return Node.objects.exclude(variety="output").exclude(variety="input")[:10]


@register_query("podsformodel", model= graphene.String(description="The pods model"), description="Gets all running pods for the Model")
class NodeWrapper(BalderObjectWrapper):
    object_type = PodType
    aslist = True

    @staticmethod
    def resolver(root, context, model):
        #TODO: Implement check before this
        return Pod.objects.accessible(context.user).filter(node__inputs__contains=[{"identifier": model}])



@register_query("node", id= graphene.ID(description="The node's ID"), description="Get a nodes in this bergen instance")
class NodeWrapper(BalderObjectWrapper):
    object_type = NodeType
    asfield = True

    @staticmethod
    def resolver(root, context, id):
        return Node.objects.get(id=id)


@register_query("monitor", reference= graphene.String(description="The monitored Provision"), description="Show the status of a NOde")
class MonitorQueryWrapper(BalderObjectWrapper):
    object_type = ProvisionType
    asfield = True

    @staticmethod
    def resolver(root, context, reference):
        return Provision.objects.get(reference=reference)



@register_mutation("slot", description="Input for a Node")
class Slot(BalderMutationWrapper):
    mutation = SlotMutation




@register_query("me", description="Show the currently logged in user")
class MeQueryWrapper(BalderObjectWrapper):
    object_type = UserType
    asfield = True

    @staticmethod
    def resolver(root, context: BouncerContext):
        return context.user

@register_query("myprovisions", description="Show the currently provisions for the user")
class MeQueryWrapper(BalderObjectWrapper):
    object_type = ProvisionType
    aslist = True

    @staticmethod
    def resolver(root, context):
        print(context)
        return MyProvisions(context.user)




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

@register_mutation("assign", description="Assign Job")
class AssignMutationWrapper(BalderMutationWrapper):
    mutation = AssignMutation

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

@register_subscription("assign", description="Assign Jobs for a Pod (in one go)")
class AssignSubscriptionWrapper(BalderSubscriptionWrapper):
    ''' This provides a fast way to provide a node though a provision and moniters it on the way, violates CQRS patterns'''
    subscription = AssignSubscription

@register_subscription("check", description="Monitor a Job for changes")
class MonitorSubscriptionWrapper(BalderSubscriptionWrapper):
    ''' This provides a fast way to provide a node though a provision and moniters it on the way, violates CQRS patterns'''
    subscription = CheckSubscription