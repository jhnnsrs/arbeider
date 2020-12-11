from rest_framework import serializers

from delt.models import *


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


class ProvisionMessageSerializer(serializers.Serializer):
    provision = serializers.PrimaryKeyRelatedField(queryset=Provision.objects.all())


class AssignationMessageSerializer(serializers.Serializer):
    assignation = serializers.PrimaryKeyRelatedField(queryset=Assignation.objects.all())

class ProvisionModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Provision
        fields = "__all__"

class AssignationModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assignation
        fields = "__all__"
