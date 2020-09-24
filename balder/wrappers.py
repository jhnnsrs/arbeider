from balder.mutations.base import BaseMutation
from balder.queries.base import BaseQuery
from balder.subscriptions.base import BaseSubscription


class WrappingError(Exception):
    pass

class BalderObjectWrapper(object):
    object_type = None
    resolver = None
    aslist = False
    asfield = False
    withfilter = False


class BalderQueryWrapper(object):
    query = None

    def __init__(self, *args, **kwargs):
        if self.query is None or not issubclass(self.query, BaseQuery):
            raise WrappingError("BalderQueryWrapper must provide a BaseQuery as field: subscription")
        
        self._type = self.query

    def get_object(self):
        return self._type


    def get_description(self):
        return None


class BaseSubscriptionWrapper(object):
    pass

    def get_description(self):
        return None

    def get_object(self):
        raise NotImplementedError("BaseSubscriptionWrapper ist an abstract base class. Do Not Implement Directly")


class BalderSubscriptionWrapper(BaseSubscriptionWrapper):
    subscription = None

    def __init__(self, *args, **kwargs):
        if self.subscription is None or not issubclass(self.subscription, BaseSubscription):
            raise WrappingError("SubscpritionWrapper must provide a BaseSubscription as field: subscription")
        
        self._type = self.subscription

    def get_object(self):
        return self._type

class BalderBuildableSubscriptionWrapper(BaseSubscriptionWrapper):
    subscriptionBuilder = None

    def __init__(self, *args, **kwargs):
        if self.subscriptionBuilder is None or not callable(self.subscriptionBuilder):
            raise WrappingError("BuildableSubscpritionWrapper must provide a callable as field: subscription")
        
        self._type = self.subscriptionBuilder(*args, **kwargs)

    def get_object(self):
        return self._type

class BalderMutationWrapper(object):
    mutation = None

    def __init__(self, *args, **kwargs):
        if self.mutation is None or not issubclass(self.mutation, BaseMutation):
            raise WrappingError("MutationWrapper must provide a BaseMutation as field: mutation")
        
        self._type = self.mutation

    def get_object(self):
        return self._type

    def get_description(self):
        return None


