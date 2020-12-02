import logging

from django.core.management import BaseCommand
import os
from delt.discover import autodiscover_routers, autodiscover_pods, autodiscover_nodes

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)


    def handle(self, *args, **options):
        """If Delt Register is set to True, autoDiscoverConsumers will
        always register Workers with the Backend, here we turn it on just for the Moment"""

        logger.debug("Starting to discover")

        
        autodiscover_nodes(catalog=True)
        autodiscover_pods(register=False, catalog=True)
        #autodiscover_routes(catalog=True)
        logger.info("DONE - Restart")