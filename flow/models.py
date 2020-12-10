from delt.utils import generate_random_name
import uuid

from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH

from delt.models import Node, Route, Template


class Graph(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    version = models.CharField(max_length=100, default="1.0alpha")
    name = models.CharField(max_length=100, null=True, default=generate_random_name)
    diagram = models.JSONField()
    description = models.CharField(max_length=50000, default="Add a Description")

    def __str__(self):
        return f"{self.name}"

class FlowNode(Node):

    def __str__(self):
        return f"{self.name} with Graph ü self.graph"

class Engine(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"Engine: {self.name}"


class Flow(Template):
    diagram = models.JSONField()
    engine= models.ForeignKey(Engine, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.name} for {self.engine}"


class CompilerRoute(models.Model):
    type = models.CharField(max_length=100, default="validate")
    operation_name = models.CharField(max_length=2000, default="void")


class Compiler(models.Model):
    name = models.CharField(max_length=1000, default=generate_random_name)
    validation_endpoint = models.ForeignKey(CompilerRoute, on_delete=models.CASCADE, null=True, blank=True)


class ExecutionGraph(models.Model):
    name = models.CharField(max_length=1000, default=generate_random_name)
    version = models.CharField(max_length=200, default="standard")