from django.contrib.auth.models import User, Group
from django.db import models
from delt.models import Node
# Create your models here.


class KonfigNode(Node):

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.identifier)

