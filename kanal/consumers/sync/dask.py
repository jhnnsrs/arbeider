from kanal.consumers.sync.base import KanalSyncConsumer
from kanal.schedulers import get_default_scheduler, DEFAULT_SCHEDULERS
import logging

logger = logging.getLogger(__name__)


class DaskKanalSyncConsumer(KanalSyncConsumer):
    enabled_schedulers = DEFAULT_SCHEDULERS
    scheduler_priority = DEFAULT_SCHEDULERS

    def __init__(self, scope):
        logger.info(f"{self.__class__.__name__} will be able to access these schedulers {repr(self.enabled_schedulers)}")
        super().__init__(scope)

    
    def compute(self, graph, wanted= None):
        return graph.compute(scheduler=get_default_scheduler())

    def persist(self, graph):
        return graph.persist(scheduler=get_default_scheduler())
