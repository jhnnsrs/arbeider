import uuid

from rest_framework import serializers
from delt.params import CharField, ModelField, FilteredModelField, Inputs
from delt.models import Pod, Node


class JobConfig(serializers.Serializer):
    instance = CharField(default=uuid.uuid4)
    pod = ModelField(Pod, allow_null=True)






def job_config_builder(node: Node, theinputs):

    class JobTestConfig(serializers.Serializer):
        instance = CharField(default=uuid.uuid4)
        pod = FilteredModelField(Pod, {"node": node}, allow_null=True)
        inputs = theinputs()

    return JobTestConfig