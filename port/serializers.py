from django.contrib.auth import get_user_model
from rest_framework import serializers

from delt.models import Node, Pod, Provision

# pong
class ProvisionRequestSerializer(serializers.Serializer):
    node = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())
    selector = serializers.CharField(max_length=1000)
    parent = serializers.PrimaryKeyRelatedField(queryset=Provision.objects.all(), required=False) #The reference in Ports case is its channel + a unique code
    reference = serializers.CharField(max_length=1000) #The reference in Ports case is its channel + a unique code
    token = serializers.CharField(max_length=1000)

#pong
class AssignationRequestSerializer(serializers.Serializer):
    reference = serializers.CharField(max_length=4000)
    inputs = serializers.JSONField()
    pod = serializers.PrimaryKeyRelatedField(queryset=Pod.objects.all())
    token = serializers.CharField(allow_null=False)






class InitRequestSerializer(serializers.Serializer):
    pod = serializers.PrimaryKeyRelatedField(queryset=Pod.objects.all())


class ActivationRequestSerializer(serializers.Serializer):
    pod = serializers.PrimaryKeyRelatedField(queryset=Pod.objects.all())