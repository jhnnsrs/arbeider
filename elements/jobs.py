from jobb.registry import register_with_job_routes
from jobb.viewsets import JobRouteViewSet

from .nodes.configs.watchers.sample import SampleWatcherConfig

@register_with_job_routes(SampleWatcherConfig)
class SampleWatcherViewSet(JobRouteViewSet):
    pass
