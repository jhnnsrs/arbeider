import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers

from delt.consumers.config import (CONSUMER_ASSIGNATION_ACTION,
                                    GATEWAY_PROVISION_UPDATE,
                                   CONSUMER_PROVISION_ACTION, GATEWAY_CHANNEL,
                                   GATEWAY_POD_PROVISION_FAILURE_ACTION,
                                   GATEWAY_POD_PROVISION_SUCCESS_ACTION)
from delt.serializers import AssignationSerializer, ProvisionSerializer

channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)


def deserialized(serializer: serializers.Serializer, raise_exception=True):

    def real_decorator(function):

        def wrapper(self, message):
            serialized = serializer(data=message["data"])
            if serialized.is_valid(raise_exception=raise_exception):
                data = serialized.validated_data
                function(self, data)
        return wrapper

    return real_decorator


def send_provision_to_gateway(provision):
    logger.debug(f"Received provision result from {provision['provider']}: {provision}")
    serialized = ProvisionSerializer(provision)
    async_to_sync(channel_layer.send)(GATEWAY_CHANNEL, {"type": GATEWAY_PROVISION_UPDATE, "data": serialized.data})

def send_unprovision_to_gateway(unprovision):
    logger.debug(f"Received unprovision result from {unprovision['provider']}: {unprovision}")
    serialized = ProvisionSerializer(unprovision)
    if "error" in unprovision and "error" is not None:
        async_to_sync(channel_layer.send)(GATEWAY_CHANNEL, {"type": GATEWAY_POD_UNPROVISION_FAILURE_ACTION, "data": serialized.data})
    if "pod" in unprovision and "pod" is not None:
        async_to_sync(channel_layer.send)(GATEWAY_CHANNEL, {"type": GATEWAY_POD_UNPROVISION_SUCCESS_ACTION, "data": serialized.data})


def send_provision_to_channel(consumer, provision):
    logger.info(f"Sending provision to Consumer at channel {consumer}: {provision}")
    serialized = ProvisionSerializer(provision)
    async_to_sync(channel_layer.send)(consumer, {"type": CONSUMER_PROVISION_ACTION, "data": serialized.data})


def send_assignation_to_channel(channel, assignation):
    logger.info(f"Sending assignation to Consumer at channel {channel}: {assignation}")
    serialized = AssignationSerializer(assignation)
    async_to_sync(channel_layer.send)(channel, {"type": CONSUMER_ASSIGNATION_ACTION, "data": serialized.data})