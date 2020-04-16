from test.models import *

from django.contrib.auth.models import User
from django.db import models

from delt.models import Job, Node
# Create your models here.
from elements.models import ROI, Experiment, Sample, Transformation


class Tester(Node):

    def __str__(self):
        return "Tester at Path {1}".format(self.name, self.channel)

class Testing(Job):
    tester = models.ForeignKey(Tester, on_delete=models.CASCADE)

    def __str__(self):
        return "Test for Testing: {0}".format(self.tester.name)
