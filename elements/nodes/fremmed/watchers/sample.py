from fremmed.registry import FrontendNodeType, register_with_fremmed_backend
from elements.nodes.configs.watchers.sample import SampleWatcherConfig


@register_with_fremmed_backend(SampleWatcherConfig)
class SampleWatcher(FrontendNodeType):
    interface = "watcher/sample"
    config = SampleWatcherConfig
    name = "Sample Watcher"
    path = "SampleWatcher"
    settings = {"rescale": True}