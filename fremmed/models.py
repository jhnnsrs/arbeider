import uuid
from delt.models import Pod
from django.db import models
from fremmed.fields import AccessPolicy

class FrontendPod(Pod):
    path = models.CharField(max_length=1000, unique=True, help_text="The Path this Frontend Node listenes to")
    gate = models.CharField(max_length=1000, unique=True, help_text="The Gate ID of this Pod", default= uuid.uuid4)
    access = AccessPolicy()

    def __str__(self):
        return f"Pod for Node {self.node.name} on path {self.path} and Gate {self.gate}"



