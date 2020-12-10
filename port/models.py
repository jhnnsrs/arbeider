import uuid

from django.contrib.auth.models import User, Group
from django.db import models
from delt.models import Pod, ProviderSettings, Template
from delt.utils import generate_random_name


class PortSettings(ProviderSettings):
    allow_unsafe = models.BooleanField(default=False, help_text="Allow unsafe container (Doc)")
    default_network = models.CharField(default="dev", max_length=100)


class Container(models.Model):
    image = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    repository = models.CharField(max_length=1000, default="dockerhub")

    def __str__(self) -> str:
        return f"Container {self.image}:{self.tag} from {self.repository}"


    def getDockerName(self):
        return f"{self.image}:{self.tag}"


class ContainerTemplate(Template):
    container = models.ForeignKey(Container, on_delete=models.CASCADE)

    def __str__(self):
        return f"Template {self.name} for {self.container}"


class PortPod(Pod):
    container_id = models.CharField(max_length=2000)






