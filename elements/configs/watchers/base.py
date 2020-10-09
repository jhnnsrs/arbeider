from rest_framework import serializers

from konfig.params import CharPort, Inputs, ObjectPort, Outputs
from konfig.node import Konfig


class Trigger(ObjectPort):
    type = CharPort(default="INVOCATION")

class BaseWatcherInputs(Inputs):
    trigger = Trigger()

class BaseWatcherOutputs(Outputs):
    pass


class BaseWatcherConfig(Konfig):
    package = "@canonical/elements"
    variety = "watcher"