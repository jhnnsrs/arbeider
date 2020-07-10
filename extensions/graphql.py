import graphene
from django.forms.models import model_to_dict
from graphene.types.generic import GenericScalar

from balder.delt_types import JobType, NodeType, PodType, ProvisionType
from balder.mutations.assignations.assign import AssignMutation
from balder.mutations.provisions.provide import ProvideMutation
from balder.queries.provisions.monitor import MonitorQuery
from balder.register import (register_mutation, register_query,
                             register_subscription)
from balder.subscriptions.provisions.monitor import MonitorSubscription
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

@register_query("node", id= graphene.ID(description="The node's ID"), description="Get a nodes in this bergen instance")
class NodeWrapper(BalderObjectWrapper):
    object_type = NodeType
    asfield = True

    @staticmethod
    def resolver(root, info, id):
        return Node.objects.get(id=id)


@register_query("monitor", reference= graphene.String(description="The monitored Provision"), description="Show the status of a NOde")
class MonitorQueryWrapper(BalderObjectWrapper):
    object_type = ProvisionType
    asfield = True

    @staticmethod
    def resolver(root, info, reference):
        return Provision.objects.get(reference=reference)



@register_mutation("slot", description="Input for a Node")
class Slot(BalderMutationWrapper):
    mutation = SlotMutation
    

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

@register_query("monitor2", description="Get the current state of a provision")
class MonitorQueryWrapper(BalderQueryWrapper):
    ''' This provides a fast way to provide a node though a provision and moniters it on the way, violates CQRS patterns'''
    query = MonitorQuery



@register_subscription("gate", description="Gate Way")
class Gate(BalderSubscriptionWrapper):
    subscription = GateSubscription
