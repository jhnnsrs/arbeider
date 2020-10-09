
from channels.consumer import SyncConsumer
from balder.notifier.registry import get_notifying_registry

import logging

logger = logging.getLogger()

class NotifyConsumer(SyncConsumer):

    def on_notify(self, message: dict):
        registry = get_notifying_registry()
        data = message["data"]
        subscriptionClass = registry.getSubscriptionForUUID(data["uuid"])
        for reference in data["references"]:
            subscriptionClass.broadcast(group=reference,payload="initialPayload")