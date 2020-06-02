import uuid
from delt.models import Pod
from django.db import models
from fremmed.fields import AccessPolicy

class FrontendPod(Pod):
    gate = models.CharField(max_length=1000, unique=True, help_text="The Gate ID of this Pod", default= uuid.uuid4)
    access = AccessPolicy(default=dict)

    def __str__(self):
        return f"Pod for Node {self.node.name} ond Gate {self.gate}"

    class Meta:
        permissions = (
            ('access_pod', 'The user can host this Pod'),
        )



