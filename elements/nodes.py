from delt.nodes.default import ConfigNode, register_node
from elements.configs.watchers.sample import SampleWatcherConfig


@register_node(SampleWatcherConfig)
class SampleWatcher(ConfigNode):
    pass