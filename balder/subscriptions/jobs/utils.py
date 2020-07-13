from balder.subscriptions.jobs.check import CheckSubscription
from balder.subscriptions.jobs.assign import AssignSubscription
from delt.serializers import AssignationMessageSerializer, ProvisionSerializer


def to_balder_assignation_listeners(assignation):
    serialized = AssignationMessageSerializer({"assignation":assignation})
    print(f"Sending to the consumers {assignation.reference}")
    AssignSubscription.broadcast(group=f"{assignation.reference}",payload=serialized.data)
    CheckSubscription.broadcast(group=f"{assignation.reference}",payload=serialized.data)
