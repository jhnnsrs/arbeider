from delt.models import DataPoint
from balder.delt.enums import ClientTypeEnum
from delt.extension.models import get_extension_models
import logging
import uuid
import os
import graphene
from django.conf import settings
import time
import datetime

from balder.delt.transcripts import TranscriptType
from balder.mutations.base import BaseMutation
from balder.utils import modelToDict

logger = logging.getLogger(__name__)


from django.apps import apps




class NotNodeFoundError(Exception):
    pass

class NegotiateMutation(BaseMutation):
    Output = TranscriptType

    class Arguments:
        client_type = graphene.Argument(ClientTypeEnum, description="The clients type [external, ...]")

    @classmethod
    def change(cls, context, root, info, *arg, **kwargs):
        logger.warn("Negotiation incoming")
        logger.info(f"Initialized by {context.user}")


        

        transcript = {
            "extensions": {
                "array": {
                "type": "s3",
                "path": "localhost:9000",
                "params": {
                    "access_key": settings.AWS_ACCESS_KEY_ID,
                    "secret_key": settings.AWS_SECRET_ACCESS_KEY
                }
            },
            },
            "communication": {
                "type" : "grapqhl",
                "url": "http://localhost:8000/graphql"
            },
            "models": get_extension_models(),
            "points": list(DataPoint.objects.all()),
            "timestamp": datetime.datetime.now(),
            "user": context.user if context.user.is_authenticated else None
        }


        return TranscriptType(**transcript)
