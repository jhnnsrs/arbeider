from django.contrib.auth import get_user_model
from delt.utils import generate_random_name
import uuid

from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH

from delt.models import Node, Route, Template



class CompilerRoute(models.Model):
    type = models.CharField(max_length=100, default="validate")
    operation_name = models.CharField(max_length=2000, default="void")


class Compiler(models.Model):
    ''' A compiler takes a certain Graph and parses it to an execution Graph'''
    name = models.CharField(max_length=1000, default=generate_random_name)
    validation_endpoint = models.ForeignKey(CompilerRoute, on_delete=models.CASCADE, null=True, blank=True)


class Graph(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    version = models.CharField(max_length=100, default="1.0alpha")
    name = models.CharField(max_length=100, null=True, default=generate_random_name)
    diagram = models.JSONField(null=True, blank=True)
    description = models.CharField(max_length=50000, default="Add a Description", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"





class ExecutionGraph(models.Model):
    ''' An exectuion graph is a form of machine readable code'''
    name = models.CharField(max_length=1000, default=generate_random_name)
    version = models.CharField(max_length=200, default="standard")