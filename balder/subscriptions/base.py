import channels_graphql_ws

class SubscriptionError(Exception):
    pass

class BaseSubscription(channels_graphql_ws.Subscription):

    class Arguments:
        abstract = True

    @classmethod
    def subscribe(cls, root, info, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def publish(cls, payload, info, *arg, **kwargs):
        raise NotImplementedError