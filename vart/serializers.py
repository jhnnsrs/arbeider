from delt.models import Assignation
from vart.models import VartPod
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField


class QueueSubscriptionMessageSerializer(serializers.Serializer):
    pod = PrimaryKeyRelatedField(queryset=VartPod.objects.all())


class HostSubscriptionMessageSerializer(serializers.Serializer):
    assignation = PrimaryKeyRelatedField(queryset=Assignation.objects.all())
