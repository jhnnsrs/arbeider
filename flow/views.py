from django.shortcuts import render
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets

from flow.models import FlowNode, Graph
from flow.serializers import FlowNodeSerializer, GraphSerializer


# Create your views here.
class FlowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = FlowNode.objects.all()
    serializer_class = FlowNodeSerializer


# Create your views here.
class GraphViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Graph.objects.all()
    serializer_class = GraphSerializer
