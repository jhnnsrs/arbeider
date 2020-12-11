from balder.subscriptions.assignation.watch import WatchSubscription
from balder.subscriptions.assignation.assign import AssignSubscription
from delt.serializers import AssignationMessageSerializer


def to_balder_assignation_listeners(assignation):
    serialized = AssignationMessageSerializer({"assignation":assignation})
    AssignSubscription.broadcast(group=f"{assignation.reference}",payload=serialized.data)
    WatchSubscription.broadcast(group=f"{assignation.reference}",payload=serialized.data)
