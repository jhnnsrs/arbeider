from balder.notifier.utils import initialPayload
from balder.notifier.registry import get_notifying_registry
from django.contrib.auth import get_user_model, user_logged_out
from django.contrib.auth.models import User
from rest_framework import serializers
from balder.delt.models import ProvisionType, UserType
from balder.subscriptions.base import BaseSubscription
import logging
import uuid

import graphene

from balder.subscriptions.provisions.base import BaseProvisionSubscription
from delt.models import Node, Provision
from delt.pipes import provision_pod_pipe, republish_provision_pipe

logger = logging.getLogger(__name__)



class MyProvisionsMessage(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

MyProvisions = lambda user: Provision.objects.filter(user=user, active=True).order_by("-created_at")[:5]


class MyProvisionsSubscription(BaseSubscription):
    Output = graphene.List(ProvisionType)
    
    class Arguments:
        pass

    @classmethod
    def accept(cls, context, root, info, *args, **kwargs):
        user = context.user
        print(f' Attaching to myprovisions_{user.id}')
        return [f'myprovisions_{user.id}']

    
    @classmethod
    def announce(cls, context, payload, *arg, **kwargs):
        logger.info("Publishing it to the MyProvisions")


        serializer = MyProvisionsMessage(data=payload)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            return MyProvisions(user)



def to_balder_myprovisions(provision):
    message = MyProvisionsMessage({"user":provision.user})
    group= f'myprovisions_{provision.user.id}'
    print(f"publishing to {group}")
    MyProvisionsSubscription.broadcast(group=group,payload=message.data)