import channels_graphql_ws

from delt.bouncers.context import BouncerContext


class SubscriptionError(Exception):
    pass

class BaseSubscription(channels_graphql_ws.Subscription):

    class Arguments:
        abstract = True

    @classmethod
    def accept(cls, context: BouncerContext, root, info, *args, **kwargs) -> [str]:
        raise NotImplementedError("Please override the accept method in your BaseSubscription")

    @classmethod
    def subscribe(cls, root, info, *args, **kwargs):
        context = BouncerContext(info=info)
        return cls.accept(context, root, info, *args, **kwargs)

    @classmethod
    def publish(cls, payload, info, *arg, **kwargs):
        raise NotImplementedError