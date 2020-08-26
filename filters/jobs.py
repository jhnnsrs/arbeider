from jobb.registry import register_with_job_routes
from jobb.viewsets import JobRouteViewSet

from .configs.projections.maxisp import MaxISPConfig
from .configs.filters.blur import BlurFilterKonfig
from .configs.filters.prewitt import PrewittFilterKonfig


@register_with_job_routes(MaxISPConfig)
class MaxISPViewSet(JobRouteViewSet):
    pass

@register_with_job_routes(BlurFilterKonfig)
class BlurViewSet(JobRouteViewSet):
    pass

@register_with_job_routes(PrewittFilterKonfig)
class PrewittFilter(JobRouteViewSet):
    pass