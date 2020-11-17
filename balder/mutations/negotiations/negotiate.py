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


class NotNodeFoundError(Exception):
    pass

class NegotiateMutation(BaseMutation):
    Output = TranscriptType

    class Arguments:
        client_type = graphene.String(required=True, description="The clients type [external, ...]")

    @classmethod
    def change(cls, context, root, info, *arg, **kwargs):
        logger.warn("Negotiation incoming")
        logger.info(f"Initialized by {context.user}")


        transcript = {
            "array": {
                "type": "s3",
                "path": settings.S3_PUBLIC_DOMAIN,
                "params": {
                    "access_key": settings.AWS_ACCESS_KEY_ID,
                    "secret_key": settings.AWS_SECRET_ACCESS_KEY
                }
            },
            "communication": {
                "type" : "grapqhl",
                "url": "http://localhost:8000/graphql"
            },
            "timestamp": datetime.datetime.now(),
            "user": context.user
        }


        return TranscriptType(**transcript)
