import logging

from balder.delt.models import (AssignationType)
from balder.subscriptions.base import BaseSubscription
from delt.serializers import (AssignationMessageSerializer,)

logger = logging.getLogger(__name__)


class BaseAssignationSubscription(BaseSubscription):
    Output = AssignationType

    @classmethod
    def announce(cls, context, payload, *arg, **kwargs):
        logger.info("Publishing it to the Assignation Watchers")
        serializer = AssignationMessageSerializer(data=payload)
        if serializer.is_valid():
            assignation = serializer.validated_data["assignation"]
            return assignation
