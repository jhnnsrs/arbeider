import logging
import uuid

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.relations import PrimaryKeyRelatedField


logger = logging.getLogger(__name__)



def ModelField(model,*args, **kwargs):
    return PrimaryKeyRelatedField(queryset=model.objects.all(),*args, **kwargs)

def CharField(*args, **kwargs):
    return serializers.CharField(*args, **kwargs)

def IntField(*args, **kwargs):
    return serializers.IntegerField(*args, **kwargs)

def BoolField(*args, **kwargs):
    return serializers.BooleanField(*args, **kwargs)

class Object(serializers.Serializer):
    pass

class Inputs(serializers.Serializer):
    pass

class Outputs(serializers.Serializer):
    pass

class DummyInputs(serializers.Serializer):
    dummy = CharField(help_text= "This is just a Dummy")

class DummyOutputs(serializers.Serializer):
    dummy = CharField(help_text= "This is just a Dummy")

