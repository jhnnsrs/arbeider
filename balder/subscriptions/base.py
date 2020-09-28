import logging
from typing import List

import channels_graphql_ws
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from delt.bouncers.context import BouncerContext

channel_layer = get_channel_layer()
logger = logging.getLogger()


class SubscriptionError(Exception):
    pass

class BaseSubscription(channels_graphql_ws.Subscription):
    initialPayloadHook = None
    subscriptionUUID = None


    class Arguments:
        abstract = True

    @classmethod
    def accept(cls, context: BouncerContext, root, info, *args, **kwargs) -> List[str]:
        raise NotImplementedError("Please override the accept method in your BaseSubscription")

    @classmethod
    def subscribe(cls, root, info, *args, **kwargs):
        context = BouncerContext(info=info)

        references = cls.accept(context, root, info, *args, **kwargs)
        if cls.initialPayloadHook is not None:
            assert cls.subscriptionUUID is not None, "Please provide a subscription UUID in order to USE the notifier"
            message = {"type": "on_notify", "data" : {"uuid": cls.subscriptionUUID, "references": references}}
            logging.debug(f"Send initial Payload notification to {cls.subscriptionUUID}")
            async_to_sync(channel_layer.send)("thenotifier", message )


        return references

    @classmethod
    def announce(cls, context, payload, *args, **kwargs):
        raise NotImplementedError
    

    @classmethod
    def publish(cls, payload, info, *args, **kwargs):
        context = BouncerContext(info=info)
        if payload == "initialPayload":
            return cls.initialPayloadHook(context, info, *args, **kwargs)
        else:
            return cls.announce(context, payload, *args, **kwargs)
