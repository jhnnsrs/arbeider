from django.db import models
from port.models import ContainerTemplate, PortPod
from delt.models import Node, Pod, ProviderSettings, Template
# Create your models here.
import uuid

class VartSettings(ProviderSettings):
    allow_public = models.BooleanField(default=False, help_text="Allow Public Clients?")



class Volunteer(Template):
    active = models.BooleanField(help_text="Is this volunteer active right now", default=False)
    identifier = models.UUIDField(default=uuid.uuid4, help_text="The identifier for this volunteer")

    def __str__(self) -> str:
        return f"Volunteer for node {self.node.name}"


class VartPod(Pod):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)