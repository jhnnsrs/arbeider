import logging
import uuid

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.relations import PrimaryKeyRelatedField


logger = logging.getLogger(__name__)

def paramfield(raise_exception=True):

    def real_decorator(function):

        def wrapper(*args, **kwargs):
            help_text = kwargs.pop("help_text") if "help_text" in kwargs else ""
            if "info" in kwargs: help_text += kwargs.pop("info")
            if "description" in kwargs: help_text += "||" + kwargs.pop("description")
            return function(*args, **kwargs, help_text=help_text)
        
        return wrapper

    return real_decorator

@paramfield()
def ModelField(model, *args, **kwargs):
    return PrimaryKeyRelatedField(queryset=model.objects.all(),*args, **kwargs)

@paramfield()
def CharField(*args, **kwargs):
    return serializers.CharField(*args, **kwargs)

@paramfield()
def IntField(*args, **kwargs):
    return serializers.IntegerField(*args, **kwargs)

@paramfield()
def FloatField(*args, **kwargs):
    return serializers.FloatField(*args, **kwargs)

@paramfield()
def ListField(*args, **kwargs):
    return serializers.ListField(*args, **kwargs)

@paramfield()
def BoolField(*args, **kwargs):
    return serializers.BooleanField(*args, **kwargs)



class Model(serializers.ModelSerializer):

    class Meta:
        abstract= True


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


def FilteredModelField(model, filterkwargs, *args, **kwargs):
    return PrimaryKeyRelatedField(queryset=model.objects.filter(**filterkwargs).all(),*args, **kwargs)