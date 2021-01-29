from delt.models import Assignation
from delt.messages.assignation import AssignationMessage
import logging

from balder.delt.models import (AssignationType)
from balder.subscriptions.base import BaseSubscription
from delt.serializers import (AssignationMessageSerializer,)

logger = logging.getLogger(__name__)


class BaseAssignationSubscription(BaseSubscription):
    Output = AssignationType

    @classmethod
    def announce(cls, context, payload, *arg, **kwargs):
        print(payload)
        assignation = AssignationMessage(**payload)
        logger.info("Publishing it to the Assignation Watchers")
        return Assignation.objects.get(id=assignation.data.id)
