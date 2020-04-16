import uuid

from rest_framework import serializers
from delt.params import CharField


class JobConfig(serializers.Serializer):
    instance = CharField(default=uuid.uuid4)