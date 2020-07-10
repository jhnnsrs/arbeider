from rest_framework import serializers

from flow.models import FlowNode, Graph


class FlowNodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FlowNode
        fields = "__all__"



class GraphSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Graph
        fields = "__all__"