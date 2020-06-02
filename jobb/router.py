import logging

from django.db import ProgrammingError
from rest_framework.routers import DefaultRouter, APIRootView

from delt.discover import autodiscover_routers
from delt.registry import get_registry

logger = logging.getLogger(__name__)


class JobsRootView(APIRootView):
    """
    Jobs are a clean way to deal with a few common issues
    """

    def get_view_name(self) -> str:
        return "Jobs"



class JobRouter(DefaultRouter):
    APIRootView = JobsRootView

    def __init__(self, *args, **kwargs):
        try:
            autodiscover_routers(catalog=True,register=True)
        except Exception as e:
            logger.error(f"Job Router was not able to Setup! Did you run Migrations? {e}")
            raise e
        super().__init__(*args, **kwargs)

        for key, route in get_registry().getViewsetRoutes().items():
            self.register(route["route"], route["viewset"], basename=key)
        


router = JobRouter()