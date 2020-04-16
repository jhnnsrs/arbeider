from jobb.registry import register_with_job_routes
from jobb.viewsets import JobRouteViewSet

from .nodes.configs.projections.maxisp import MaxISPConfig
from .nodes.configs.filters.blur import BlurFilterConfig
from .nodes.configs.filters.prewitt import PrewittFilterConfig


@register_with_job_routes(MaxISPConfig)
class MaxISPViewSet(JobRouteViewSet):
    pass

@register_with_job_routes(BlurFilterConfig)
class BlurViewSet(JobRouteViewSet):
    pass

@register_with_job_routes(PrewittFilterConfig)
class PrewittFilter(JobRouteViewSet):
    pass