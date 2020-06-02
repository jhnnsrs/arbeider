from delt.models import Pod
from django.db import models

class KanalPod(Pod):
    channel = models.CharField(max_length=1000, unique=True, help_text="The Channel this Node listenes to")

    def __str__(self):
        return f"Kanal Pod for {self.node.package}/{self.node.interface} on Kanal {self.channel}"
