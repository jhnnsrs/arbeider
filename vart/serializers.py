from vart.models import VartPod
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField


class QueueSubscriptionMessageSerializer(serializers.Serializer):
    pod = PrimaryKeyRelatedField(VartPod)
