from arbeid.settings import ARNHEIM_HOST
from delt.enums import Endpoint
from delt.models import DataPoint
from delt.registries.registry import BaseRegistry
from delt.handlers.newbase import BaseHandler
import logging
from django.conf import settings
logger = logging.getLogger(__name__)

datapointregistry = None

class DataPointRegistry(BaseRegistry):

    def __init__(self) -> None:
        self.pointnameDatapointMap: dict[str, DataPoint] = {}

    def registerDataPoint(self,name, host=settings.ARNHEIM_HOST, type=Endpoint.GRAPHQL, port=settings.ARNHEIM_PORT):
        datapoint = None
        try:
            datapoint = DataPoint.objects.update_or_create(name=name, defaults= {"host": host, "type": type, "port": port} )
        except Exception as e:
            logger.error("MIGRATE FIRST")

        self.pointnameDatapointMap[name] = datapoint

    def getDatapointForName(self, name):
        return self.pointnameDatapointMap[name]




def get_datapoint_registry() -> DataPointRegistry:
    global datapointregistry
    if datapointregistry is None:
        datapointregistry = DataPointRegistry()
    return datapointregistry