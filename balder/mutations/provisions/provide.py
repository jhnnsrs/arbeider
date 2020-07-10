import logging
import uuid

import graphene
from django.forms.models import model_to_dict
from rest_framework import serializers

from balder.delt_types import NodeType, PodType, UserType
from balder.mixins import ProvisionFieldsMixin
from balder.mutations.base import BaseMutation
from balder.subscriptions.base import BaseSubscription
from balder.utils import modelToDict
from delt.bouncers.context import BouncerContext
from delt.context import Context
from delt.models import Node, Pod, Provision
from balder.delt_types import Node, Pod, ProvisionType
from delt.pipes import provision_pod_pipe
from delt.serializers import (PodSerializer, ProvisionModelSerializer,
                              ProvisionSerializer)

logger = logging.getLogger(__name__)


class NotNodeFoundError(Exception):
    pass

class ProvideMutation(BaseMutation, ProvisionFieldsMixin):
    Output = ProvisionType

    class Arguments:
        node = graphene.ID(required=True, description="The node's id")
        reference = graphene.String(required=False, description="This Pods unique Reference (for the Client)")
        parent = graphene.String(required=False, description="The parent provision")
        selector = graphene.String(required=False, description="The SelectorString")

    @classmethod
    def change(cls, context, root, info, *arg, **kwargs):
        logger.info("Publishing it to the Consumer")

        reference = kwargs.pop("reference") if "reference" in kwargs else uuid.uuid4()
        nodeid = kwargs.pop("node") if "node" in kwargs else None
        parent = kwargs.pop("parent") if "parent" in kwargs else None
        selector = kwargs.pop("selector") if "selector" in kwargs else "__auto__"

        try:
            node = Node.objects.get(id=nodeid)
        except:
            raise NotNodeFoundError("Please specifiy a correct NodeID")
        
        provision = provision_pod_pipe(context, reference, node, selector, parent)

        kwargs = modelToDict(provision)
        return ProvisionType(**kwargs)