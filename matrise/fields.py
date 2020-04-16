from django.conf import settings
from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from matrise.stores import XArrayStore

class StoreField(models.FileField):
    attr_class = XArrayStore
    description = "XArrayStore"


class ShapeField(ArrayField):
    pass


class DimsField(ArrayField):
    pass
