from delt.models import ProviderSettings
from flow.models import Compiler, ExecutionGraph
from port.models import Container, ContainerTemplate, PortPod, PortSettings
from django.db import models
import uuid
# Create your models here.



class RxSettings(PortSettings):
    engine = models.ForeignKey(Container, on_delete=models.CASCADE)

class RxCompiler(Compiler):
    pass

    def __str__(self) -> str:
        return f"{self.name}"


class RxGraph(ExecutionGraph):
    value = models.JSONField()


class RxTemplate(ContainerTemplate):
    graph = models.ForeignKey(RxGraph, on_delete=models.CASCADE, help_text="The RxGraph atached to this potential Worker")
    identifier = models.UUIDField(default=uuid.uuid4, help_text="The identifier for this volunteer")

    def __str__(self) -> str:
        return f"Rxtemplate for graph {self.graph}"


class RxPod(PortPod):
    
    def __str__(self):
        return f"Floly pod for Rx Template: {self.template}"