import uuid

from rest_framework import serializers
from delt.params import CharField


class JobConfig(serializers.Serializer):
    instance = CharField(default=uuid.uuid4)


class JobContext(object):
    scopes = []
    user = None


    def __init__(self,*args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
