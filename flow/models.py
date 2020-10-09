import uuid

from django.contrib.auth.models import Group, User
from django.db import models

from delt.models import Node, Template


class Graph(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    version = models.CharField(max_length=100, default="1.0alpha")
    name = models.CharField(max_length=100, null=True, default="Not Set")
    diagram = models.JSONField()
    description = models.CharField(max_length=50000, default="Add a Description")

    def __str__(self):
        return f"{self.name} by {self.creator}"

class FlowNode(Node):
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} for {self.graph}"


class Flow(Template):
    diagram = models.JSONField()

    def __str__(self) -> str:
        return f"{self.name} for {self.graph}"
