from rest_framework import serializers

from flow.models import Graph



class GraphSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Graph
        fields = "__all__"