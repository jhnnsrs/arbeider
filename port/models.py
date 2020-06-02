import uuid

from django.contrib.auth.models import User, Group
from django.db import models
from delt.models import Pod



class Flowly(Pod):
    container_id = models.CharField(max_length=4000)

    def __str__(self):
        return f"Pod for Flow {self.node.name} at {self.node.flownode.graph}"




