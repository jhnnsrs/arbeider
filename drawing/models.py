from django.db import models

from elements.models import ROI

# Create your models here.


class LineRoi(ROI):
    length = models.FloatField(null=False)