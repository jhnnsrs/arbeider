from delt.consumers.utils import asyncdeserialized, deserialized
from konfig.node import Konfig
import logging

from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from rest_framework import serializers

from konfig.node import Konfig
from delt.models import Job
from delt.serializers import AssignationMessageSerializer, JobSerializer
from kanal.exceptions import (KanalConsumerConfigException,
                              KanalConsumerMinorException)

logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()



class KanalAsyncConsumer(AsyncConsumer):
    konfig: Konfig  = None
    jobSerializer = JobSerializer

    def __init__(self):
        if self.konfig is None or not issubclass(self.konfig, Konfig):
            print("Something going wrong")
            raise KanalConsumerConfigException(f"{self.__class__.__name__} was not registered with a Node")

        super().__init__()


    async def progress(self, message):
        logger.info(f"Progress {message}")
        self.assignation.status = f"progress: {message}"
        self.assignation.save()

        serialized = AssignationMessageSerializer({"assignation": self.assignation})
        channel_layer.send("assignation_progress",serialized.data)

    @sync_to_async
    def get_inputs(self, inputsjson, raise_exception=True):
        inputs: serializers.Serializer = self.konfig.inputs(data=inputsjson)
        if inputs.is_valid(raise_exception=raise_exception):
            return inputs


    @asyncdeserialized(AssignationMessageSerializer)
    async def assign(self, message ):
        self.assignation = message["assignation"]
        inputs = await self.get_inputs(self.assignation.inputs)
        
        outputdict = await self.start(inputs.validated_data)

        print(outputdict)
        # Serialize the outputs
        outputs = self.konfig.outputs(outputdict)
        self.assignation.status = "done"
        self.assignation.outputs = outputs.data
        self.assignation.save()
        # Send them Back
        serialized = AssignationMessageSerializer({"assignation": self.assignation})
        channel_layer.send("assignation_done",serialized.data)
        

    async def start(self, inputs: dict):
        """ 
        Should Return the outputs as a dict

        """
        raise NotImplementedError



