import logging

from channels.consumer import AsyncConsumer, SyncConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from rest_framework import serializers

from delt.models import Job
from delt.node import NodeConfig
from delt.serializers import JobSerializer
from delt.status import JobStatus, buildProgressStatus
from kanal.exceptions import (KanalConsumerConfigException,
                              KanalConsumerMinorException)

logger = logging.getLogger(__name__)


class KanalAsyncConsumer(AsyncConsumer):
    config: NodeConfig  = None
    jobSerializer = JobSerializer

    def __init__(self, scope):
        if self.config is None or not issubclass(self.config, NodeConfig):
            raise KanalConsumerConfigException(f"{self.__class__.__name__} was not registered with a Node")

        super().__init__(scope)

