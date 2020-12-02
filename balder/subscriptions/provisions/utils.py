from balder.subscriptions.provisions.monitor import MonitorSubscription
from balder.subscriptions.provisions.provide import ProvideSubscription
from delt.serializers import ProvisionMessageSerializer, ProvisionSerializer


def to_balder_provision_listeners(provision):
    serialized = ProvisionMessageSerializer({"provision":provision})
    ProvideSubscription.broadcast(group=f"{provision.reference}",payload=serialized.data)
    MonitorSubscription.broadcast(group=f"{provision.reference}",payload=serialized.data)
