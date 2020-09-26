from rest_framework import serializers

from konfig.params import CharField, Inputs, Object, Outputs
from konfig.node import Konfig


class Trigger(Object):
    type = CharField(default="INVOCATION")

class BaseWatcherInputs(Inputs):
    trigger = Trigger()

class BaseWatcherOutputs(Outputs):
    pass


class BaseWatcherConfig(Konfig):
    package = "@canonical/elements"
    variety = "watcher"