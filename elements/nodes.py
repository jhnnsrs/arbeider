from konfig.backend import register_konfig_node
from elements.configs.watchers.sample import SampleWatcherConfig


@register_konfig_node(SampleWatcherConfig)
class SampleWatcher(object):
    pass