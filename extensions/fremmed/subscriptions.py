import graphene
from graphene.types.generic import GenericScalar
from guardian.shortcuts import get_perms
from balder.delt_types import PodType, UserType
from balder.subscriptions.base import BaseSubscription
from balder.utils import serializerToDict
from delt.context import Context
from delt.models import Pod
from delt.serializers import JobSerializer, PodSerializer
from delt.settingsregistry import get_settings_registry
from fremmed.models import FrontendPod


class GateError(Exception):
    pass

class GateSubscription(BaseSubscription):
    handler = "fremmed"
    inputs = GenericScalar()
    outputs = GenericScalar()
    reference = graphene.String()
    selector = graphene.String()
    pod = graphene.Field(PodType)
    creator = graphene.Field(UserType)
    unique = graphene.UUID()
    settings = GenericScalar()
    id = graphene.ID()
    unique = graphene.String()
    statusmessage = graphene.String()
    statuscode = graphene.Int()

    class Arguments:
        unique = graphene.String(required=True, description="Pods unique Identifier")
        

    @classmethod
    def subscribe(cls, root, info, *args, **kwargs):

        # Check If User is authorized
        unique = kwargs["unique"]
        context = Context(info=info)
        user = context.user
        pod = FrontendPod.objects.get(unique=unique)
        
        if 'access_pod' in get_perms(user, pod):
            get_settings_registry().getHandlerForProvider("fremmed").on("activate_pod")(pod)
            return [f"gate_{unique}"]
        else:
            raise GateError("User does not have the necessary Permissions")

    @classmethod
    def publish(cls, payload, info, *arg, **kwargs):
        serialized = JobSerializer(data=payload)
        job_dict = serializerToDict(serialized)
        inputs = job_dict.pop("args")
        return cls(**job_dict, inputs=inputs)