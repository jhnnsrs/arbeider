from jobb.registry import register_with_job_routes
from jobb.viewsets import JobRouteViewSet

from .configs.projections.maxisp import MaxISPConfig
from .configs.filters.blur import BlurFilterConfig
from .configs.filters.prewitt import PrewittFilterConfig


@register_with_job_routes(MaxISPConfig)
class MaxISPViewSet(JobRouteViewSet):
    pass

@register_with_job_routes(BlurFilterConfig)
class BlurViewSet(JobRouteViewSet):
    pass

@register_with_job_routes(PrewittFilterConfig)
class PrewittFilter(JobRouteViewSet):
    pass