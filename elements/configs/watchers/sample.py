from delt.params import BoolField, Inputs, IntField, ModelField
from elements.models import ROI, Representation, Sample
from elements.configs.watchers.base import (BaseWatcherConfig,BaseWatcherOutputs,
                                                  BaseWatcherInputs)


class SampleWatcherOutputs(BaseWatcherOutputs):
    sample = ModelField(Sample, help_text="The watched Sample")

class SampleWatcherConfig(BaseWatcherConfig):
    name="Sample Watcher"
    path = "Sample-Watcher"
    interface = "sample-watcher"
    inputs = BaseWatcherInputs
    outputs = SampleWatcherOutputs