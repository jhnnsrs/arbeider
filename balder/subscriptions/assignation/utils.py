from balder.subscriptions.assignation.watch import WatchSubscription
from balder.subscriptions.assignation.assign import AssignSubscription
from delt.serializers import AssignationMessageSerializer, ProvisionSerializer


def to_balder_assignation_listeners(assignation):
    serialized = AssignationMessageSerializer({"assignation":assignation})
    print(f"Sending to the consumers {assignation.reference}")
    AssignSubscription.broadcast(group=f"{assignation.reference}",payload=serialized.data)
    WatchSubscription.broadcast(group=f"{assignation.reference}",payload=serialized.data)
