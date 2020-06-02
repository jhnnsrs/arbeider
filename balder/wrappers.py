from balder.builders.job_subscription import genericJobSubscriptionBuilder
from balder.builders.serializer_mutation import \
    genericSerializerMutationBuilder
from balder.delt_types import PodType
from balder.mutations.base import BaseMutation
from balder.subscriptions.base import BaseSubscription
from delt.node import NodeConfig
from konfig.node import Konfig


class WrappingError(Exception):
    pass

class BalderObjectWrapper(object):
    object_type = None
    resolver = None
    aslist = False
    asfield = False
    withfilter = False


class BaseSubscriptionWrapper(object):
    pass


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


class NodeSubscriptionWrapper(BalderBuildableSubscriptionWrapper):
    subscriptionBuilder = genericJobSubscriptionBuilder
    config: NodeConfig = None

    def __init__(self, path):
        if self.config is None or not issubclass(self.config, Konfig):
            raise NotImplementedError("Please specifiy a Node config")

        super().__init__(self.config, path)

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

class BalderBuildableMutationWrapper(object):
    mutationBuilder = None

    def __init__(self, *args, **kwargs):
        if self.mutationBuilder is None or not callable(self.mutationBuilder):
            raise WrappingError("BuildableSubscpritionWrapper must provide a callable as field: subscription")
        
        self._type = self.mutationBuilder(*args, **kwargs)

    def get_object(self):
        return self._type


class BalderSerializerMutationWrapper(BalderBuildableMutationWrapper):
    serializer_class = None
    mutationBuilder = genericSerializerMutationBuilder
    arguments = None

    def __init__(self, path, *args, **kwargs):
        if self.serializer_class is None:
            raise WrappingError("Please specifiy a serializer in your Wrapper")
        if self.arguments is not None and bool(self.arguments) is False:
            raise WrappingError(f"If you overwrite arguments please provide valid arguments for your MutationWrapper: {self.__class__.__name__}")
        super().__init__(path, self.serializer_class, self.arguments, *args, **kwargs)

    def get_object(self):
        return self._type

    def mutate(self, *args, **kwargs):
        raise NotImplementedError("Please overwrite your Mutater if you want to use it")
