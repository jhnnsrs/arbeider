import logging
import uuid

import graphene
from django.forms.models import model_to_dict
from graphene.types.generic import GenericScalar
from rest_framework import serializers

from balder.delt_types import NodeType, PodType, UserType
from balder.mixins import ProvisionFieldsMixin
from balder.mutations.base import BaseMutation
from balder.subscriptions.base import BaseSubscription
from balder.utils import modelToKwargs, serializerToDict
from delt.bouncers.context import BouncerContext
from delt.context import Context
from delt.models import Node, Pod, Provision
from delt.pipes import assign_job_pipe, provision_pod_pipe
from delt.serializers import (PodSerializer, ProvisionModelSerializer,
                              ProvisionSerializer)

logger = logging.getLogger(__name__)


class NoPodFoundError(Exception):
    pass

class AssignMutation(BaseMutation, ProvisionFieldsMixin):

    class Arguments:
        pod = graphene.ID(required=True, description="The pod's id")
        inputs = GenericScalar(required=True, description="The Inputs")
        reference = graphene.String(required=False, description="This jobs reference")

    @classmethod
    def change(cls, context, root, info, *arg, **kwargs):
        logger.info("Publishing it to the Consumer")

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        podid = kwargs.pop("pod") if "pod" in kwargs else None
        inputs = kwargs.pop("inputs") if "inputs" in kwargs else None

        try:
            pod = Pod.objects.get(id=podid)
        except:
            raise NoPodFoundError("Please specifiy a correct NodeID")
        
        assignation = assign_job_pipe(context, reference, pod, inputs)

        kwargs = modelToKwargs(assignation)
        kwargs.pop("id")
        return cls(**kwargs)