import graphene
from django.forms.models import model_to_dict
from graphene.types.generic import GenericScalar

from balder.subscriptions.provision import ProvisionSubscription
from balder.delt_types import JobType, NodeType, PodType
from balder.register import (register_mutation, register_query,
                             register_subscription)
from balder.wrappers import (BalderMutationWrapper, BalderObjectWrapper,
                             BalderSubscriptionWrapper)
from delt.models import Job, Node, Pod
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



@register_mutation("slot", description="Input for a Node")
class Slot(BalderMutationWrapper):
    mutation = SlotMutation
    



@register_subscription("provide", description="Provision Pods for Nodes")
class Provision(BalderSubscriptionWrapper):
    subscription = ProvisionSubscription


@register_subscription("gate", description="Gate Way")
class Gate(BalderSubscriptionWrapper):
    subscription = GateSubscription
