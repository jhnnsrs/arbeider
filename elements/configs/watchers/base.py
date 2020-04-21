from delt.params import Inputs,Outputs, CharField
from delt.node import NodeConfig
from rest_framework import serializers


class Trigger(serializers.Serializer):
    type = CharField(default="INVOCATION")

class BaseWatcherInputs(Inputs):
    trigger = Trigger()

class BaseWatcherOutputs(Outputs):
    pass


class BaseWatcherConfig(NodeConfig):
    package = "@canonical/elements"
    variety = "watcher"