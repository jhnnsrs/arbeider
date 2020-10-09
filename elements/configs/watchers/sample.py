from konfig.params import BoolPort, Inputs, IntPort, ModelPort
from elements.models import ROI, Representation, Sample
from elements.configs.watchers.base import (BaseWatcherConfig,BaseWatcherOutputs,
                                                  BaseWatcherInputs)


class SampleWatcherOutputs(BaseWatcherOutputs):
    sample = ModelPort(Sample, help_text="The watched Sample")

class SampleWatcherConfig(BaseWatcherConfig):
    name="Sample Watcher"
    path = "Sample-Watcher"
    interface = "sample-watcher"
    inputs = BaseWatcherInputs
    outputs = SampleWatcherOutputs