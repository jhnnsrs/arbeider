import logging
import uuid

import graphene

from balder.delt_types import NodeType, PodType, ProvisionType, UserType
from balder.mixins import ProvisionFieldsMixin
from balder.subscriptions.base import BaseSubscription
from balder.utils import modelToDict
from delt.bouncers.context import BouncerContext
from delt.context import Context
from delt.models import Node, Pod, Provision
from delt.pipes import provision_pod_pipe
from delt.serializers import (PodSerializer, ProvisionMessageSerializer,
                              ProvisionSerializer)

logger = logging.getLogger(__name__)


class BaseProvisionSubscription(BaseSubscription):
    Output = ProvisionType

    @classmethod
    def announce(cls, context, payload, *arg, **kwargs):
        logger.info("Publishing it to the Consumer")
        serializer = ProvisionMessageSerializer(data=payload)
        if serializer.is_valid():
            provision = serializer.validated_data["provision"]
            return provision