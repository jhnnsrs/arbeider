import logging

from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from rest_framework import serializers

from delt.consumers.config import (CONSUMER_ASSIGNATION_ACTION,
                                   CONSUMER_PROVISION_ACTION, GATEWAY_CHANNEL,
                                   GATEWAY_POD_PROVISION_FAILURE_ACTION,
                                   GATEWAY_POD_PROVISION_SUCCESS_ACTION,
                                   GATEWAY_PROVISION_UPDATE)
from delt.serializers import (AssignationMessageSerializer,
                              AssignationSerializer,
                              ProvisionMessageSerializer,
                              ProvisionModelSerializer, ProvisionSerializer)

channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)


def deserialized(serializer: serializers.Serializer, raise_exception=True, colapse=None):

    def real_decorator(function):

        def wrapper(self, message):
            serialized = serializer(data=message["data"])
            if serialized.is_valid(raise_exception=raise_exception):
                data = serialized.validated_data
                if colapse: data = data[colapse]
                function(self, data)
        return wrapper

    return real_decorator



def asyncdeserialized(serializer: serializers.Serializer, raise_exception=True):

    @sync_to_async
    def get_data(data):
        serialized = serializer(data=data)
        if serialized.is_valid(raise_exception=raise_exception):
            return serialized.validated_data          



    def real_decorator(function):

        async def wrapper(self, message):
            data = await get_data(message["data"])
            await function(self, data)

            
        return wrapper

    return real_decorator


def send_provision_to_gateway(provision, stream):
    logger.debug(f"Received provision result from {provision.provider}. Sending to stream {stream}: {provision}")
    serialized = ProvisionMessageSerializer({"provision":provision})
    async_to_sync(channel_layer.send)(GATEWAY_CHANNEL, {"type": stream, "data": serialized.data})

def send_assignation_to_gateway(assignation, stream):
    logger.debug(f"Received assignation result from. Sending to stream {stream}: {assignation}")
    serialized = AssignationMessageSerializer({"assignation":assignation})
    async_to_sync(channel_layer.send)(GATEWAY_CHANNEL, {"type": stream, "data": serialized.data})

def send_provision_to_channel(consumer, provision):
    logger.info(f"Sending provision to Consumer at channel {consumer}: {provision}")
    serialized = ProvisionMessageSerializer({"provision":provision})
    async_to_sync(channel_layer.send)(consumer, {"type": CONSUMER_PROVISION_ACTION, "data": serialized.data})

def send_assignation_to_channel(channel, assignation):
    logger.info(f"Sending assignation to Consumer at channel {channel}: {assignation}")
    serialized = AssignationMessageSerializer({"assignation": assignation})
    async_to_sync(channel_layer.send)(channel, {"type": CONSUMER_ASSIGNATION_ACTION, "data": serialized.data})