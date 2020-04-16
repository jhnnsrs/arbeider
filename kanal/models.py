from delt.models import Node
from django.db import models

class KanalNode(Node):
    channel = models.CharField(max_length=1000, unique=True, help_text="The Channel this Node listenes to")

    def __str__(self):
        return f"Channel Node {self.name}  ( Package: {self.package}/{self.interface} ) on Identifier {self.identifier} and Channel {self.channel}"
