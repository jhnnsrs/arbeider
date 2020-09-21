import logging
import uuid

import graphene

from balder.delt_types import (AssignationType, JobType, NodeType, PodType,
                               ProvisionType, UserType)
from balder.mixins import ProvisionFieldsMixin
from balder.subscriptions.base import BaseSubscription
from balder.utils import modelToDict
from delt.bouncers.context import BouncerContext
from delt.context import Context
from delt.models import Node, Pod, Provision
from delt.pipes import provision_pod_pipe
from delt.serializers import (AssignationMessageSerializer, PodSerializer,
                              ProvisionSerializer)

logger = logging.getLogger(__name__)


class BaseAssignationSubscription(BaseSubscription):
    Output = AssignationType

    @classmethod
    def announce(cls, context, payload, *arg, **kwargs):
        logger.info("Publishing it to the Consumer")
        serializer = AssignationMessageSerializer(data=payload)
        if serializer.is_valid():
            assignation = serializer.validated_data["assignation"]
            return assignation