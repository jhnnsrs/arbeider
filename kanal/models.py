from delt.serializers import AssignationMessageSerializer, AssignationModelSerializer
import logging
from kanal.utils import layer_send
from delt.models import Assignation, Pod, Template
from django.db import models

logger = logging.getLogger(__name__)


class KanalTemplate(Template):
    channel = models.CharField(max_length=1000, unique=True, help_text="The channel the implemtation lives on")





class KanalPod(Pod):
    channel = models.CharField(max_length=1000, unique=True, help_text="The Channel this Node listenes to")

    def __str__(self):
        return f"Kanal Pod for {self.node.package}/{self.node.interface} on Kanal {self.channel}"


    def assign(self, assignation: Assignation):
        serialized = AssignationMessageSerializer({"assignation": assignation})
        logger.info(f"Sending Assignation: {self.channel}")
        layer_send(self.channel, "assign")(serialized.data)
        return True
