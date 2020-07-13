from rest_framework import serializers

from delt.models import *


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class PodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pod
        fields = "__all__"

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['name', 'provider']



class NodeSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many=True, read_only=True)
    pods = PodSerializer(many=True, read_only=True)

    class Meta:
        model = Node
        fields = "__all__"

# FLOW Implementation

class FlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flow
        fields = "__all__"


class ProvisionSerializer(serializers.Serializer):
    node = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())
    subselector = serializers.CharField(max_length=1000)
    reference = serializers.CharField(max_length=1000)
    provider = serializers.CharField(max_length=3000)
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    error = serializers.CharField(max_length=1000, required=False)
    pod = serializers.PrimaryKeyRelatedField(queryset=Pod.objects.all(), required=False, allow_null=True)
    children = serializers.PrimaryKeyRelatedField(queryset=Provision.objects.all(), required=False, allow_null=True)
    parent = serializers.ListField(serializers.PrimaryKeyRelatedField(queryset=Provision.objects.all()), required=False, allow_null=True)

class ProvisionMessageSerializer(serializers.Serializer):
    provision = serializers.PrimaryKeyRelatedField(queryset=Provision.objects.all())

class JobMessageSerializer(serializers.Serializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())

class AssignationMessageSerializer(serializers.Serializer):
    assignation = serializers.PrimaryKeyRelatedField(queryset=Assignation.objects.all())

class ProvisionModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Provision
        fields = "__all__"



class AssignationSerializer(serializers.Serializer):
    pod = serializers.PrimaryKeyRelatedField(queryset=Pod.objects.all())
    reference = serializers.CharField(max_length=1000)
    provider = serializers.CharField(max_length=3000)
    error = serializers.CharField(max_length=1000,required=False)
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    inputs = serializers.JSONField()