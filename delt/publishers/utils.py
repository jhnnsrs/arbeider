import logging

from delt.orchestrator import get_orchestrator

logger = logging.getLogger(__name__)

def publish_to_event(event: str, *args, **kwargs):

    orchestrator = get_orchestrator()
    for publisher in orchestrator.getPublishersForEvent(event):
        logger.info(f"Publishing to {publisher.__class__.__name__} on event {event}")
        publisher.on(event)(*args, **kwargs)