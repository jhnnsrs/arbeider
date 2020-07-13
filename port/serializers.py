from django.contrib.auth import get_user_model
from rest_framework import serializers

from delt.models import Node, Pod, Provision


class ProvisionRequestSerializer(serializers.Serializer):
    node = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())
    selector = serializers.CharField(max_length=1000)
    parent = serializers.PrimaryKeyRelatedField(queryset=Provision.objects.all(), required=False) #The reference in Ports case is its channel + a unique code
    reference = serializers.CharField(max_length=1000) #The reference in Ports case is its channel + a unique code
    token = serializers.CharField(max_length=1000)


class InitRequestSerializer(serializers.Serializer):
    pod = serializers.PrimaryKeyRelatedField(queryset=Pod.objects.all())


class ActivationRequestSerializer(serializers.Serializer):
    pod = serializers.PrimaryKeyRelatedField(queryset=Pod.objects.all())