from django.db import models

from delt.models import Pod


class DebugPod(Pod):
    debug = models.BooleanField()
