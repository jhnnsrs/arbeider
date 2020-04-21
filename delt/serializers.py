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

