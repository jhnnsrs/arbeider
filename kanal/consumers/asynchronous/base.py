from konfig.node import Konfig
import logging

from channels.consumer import AsyncConsumer, SyncConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from rest_framework import serializers

from konfig.node import Konfig
from delt.models import Job
from delt.serializers import JobSerializer
from kanal.exceptions import (KanalConsumerConfigException,
                              KanalConsumerMinorException)

logger = logging.getLogger(__name__)


class KanalAsyncConsumer(AsyncConsumer):
    config: Konfig  = None
    jobSerializer = JobSerializer

    def __init__(self, scope):
        if self.config is None or not issubclass(self.config, Konfig):
            raise KanalConsumerConfigException(f"{self.__class__.__name__} was not registered with a Node")

        super().__init__(scope)

