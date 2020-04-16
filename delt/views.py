import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.hashers import get_hasher
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import Serializer
import copy

from delt.exceptions import DeltConfigError
from delt.models import *
from delt.policies import ExternalAccessPolicy
from delt.serializers import *
from due.views import PublishingModelViewSet

class NodeViewSet(PublishingModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class JobViewSet(PublishingModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator",)
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class FlowViewSet(PublishingModelViewSet):
    # MAKE THIS AN ACTION PUBLISHER THAT WILL PIPE IT THROUGH A META OBJECT CREATOR

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("creator", "group", "type")
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    publishers = [["creator"]]






