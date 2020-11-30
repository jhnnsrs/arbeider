""" The FileField Modules"""
from django.db import models
from herre.files import FieldFile

class FileField(models.FileField):
    attr_class = FieldFile
    description = "HerreFile"


