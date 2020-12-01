from django.db import models
from delt.models import Node, Pod
# Create your models here.
import uuid

class Volunteer(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, help_text="The volunteers node")
    active = models.BooleanField(help_text="Is this volunteer active right now", default=False)
    identifier = models.UUIDField(default=uuid.uuid4, help_text="The identifier for this volunteer")

    def __str__(self) -> str:
        return f"Volunteer for node {self.node.name}"


class VartPod(Pod):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
