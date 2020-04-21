import uuid

from rest_framework import serializers
from delt.params import CharField, ModelField, FilteredModelField, Inputs
from delt.models import Pod, Node


class JobConfig(serializers.Serializer):
    instance = CharField(default=uuid.uuid4)
    pod = ModelField(Pod, allow_null=True)


class JobContext(object):
    scopes = []
    user = None


    def __init__(self,*args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



def job_config_builder(node: Node, theinputs):

    class JobTestConfig(serializers.Serializer):
        instance = CharField(default=uuid.uuid4)
        pod = FilteredModelField(Pod, {"node": node}, allow_null=True)
        inputs = theinputs()

    return JobTestConfig