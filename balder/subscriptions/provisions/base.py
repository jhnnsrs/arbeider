from delt.enums import ProvisionStatus
import logging

from balder.delt.models import ProvisionType
from balder.subscriptions.base import BaseSubscription
from delt.serializers import  ProvisionMessageSerializer

logger = logging.getLogger(__name__)


class BaseProvisionSubscription(BaseSubscription):
    Output = ProvisionType

    @classmethod
    def announce(cls, context, payload, *arg, **kwargs):
        logger.info("Publishing it to the Consumer")
        serializer = ProvisionMessageSerializer(data=payload)
        if serializer.is_valid():
            provision = serializer.validated_data["provision"]
            if provision.status == ProvisionStatus.CRITICAL:
                raise Exception(provision.statusmessage)
            return provision