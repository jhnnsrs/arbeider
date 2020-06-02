from delt.settingsregistry import get_settings_registry
import logging

logger = logging.getLogger(__name__)

def publish_to_event(event: str, *args, **kwargs):
    for publisher in get_settings_registry().getPublishersForEvent(event):
        logger.info(f"Publishing to {publisher.__class__.__name__} on event {event}")
        publisher.on(event)(*args, **kwargs)