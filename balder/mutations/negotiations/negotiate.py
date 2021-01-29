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
from delt.enums import ClientType
from balder.delt.transcripts import TranscriptType
from balder.mutations.base import BaseMutation
from balder.utils import modelToDict

logger = logging.getLogger(__name__)

from django.conf import settings
from django.apps import apps
from delt.bouncers.context import BouncerContext



class NotNodeFoundError(Exception):
    pass

class NegotiateMutation(BaseMutation):
    Output = TranscriptType

    class Arguments:
        client_type = graphene.Argument(ClientTypeEnum, description="The clients type [external, ...]", required=True)

    @classmethod
    def change(cls, context: BouncerContext, root, info, *arg, **kwargs):
        logger.warn("Negotiation incoming")
        logger.info(f"Initialized by {context.user}")

        local = False
        host = settings.ARNHEIM_INWARD if local else settings.ARNHEIM_HOST
        client_type = kwargs["client_type"]


        graphql_postman = {
                "type" : "graphql",
                "kwargs" : {
                    "host" : "localhost",
                    "protocol": "wss",
                    "port": 8000,
                    "auth" : {
                        "type" : "token",
                        "token": context.token.token # We use the same token for rabbitmq as rabbitmq authenticated with token at this oauth provider
                    }
                }
        }

        pika_postman = {
                "type" : "pika",
                "kwargs" : {
                    "host" : "localhost",
                    "protocol": "wss",
                    "port": 8000,
                    "auth" : {
                        "type" : "token",
                        "token": context.token.token # We use the same token for rabbitmq as rabbitmq authenticated with token at this oauth provider
                    }
                }
        }


        transcript = {
            "extensions": {
                "array": {
                "type": "s3",
                "path": f"{host}:9000",
                "params": {
                    "access_key": settings.AWS_ACCESS_KEY_ID,
                    "secret_key": settings.AWS_SECRET_ACCESS_KEY
                }
            },
            },
            "communication": {
                "type" : "grapqhl",
                "url": f"http://{host}:8000/graphql"
            },
            "postman": pika_postman if client_type == ClientType.INTERNAL.value else graphql_postman,
            "models": get_extension_models(),
            "points": list(DataPoint.objects.all()),
            "timestamp": datetime.datetime.now(),
            "user": context.user if context.user.is_authenticated else None
        }


        return TranscriptType(**transcript)
