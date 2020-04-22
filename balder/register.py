import logging

import graphene
from channels_graphql_ws import Subscription
from django.conf import settings
from graphene_django import DjangoObjectType
from jinja2.utils import object_type_repr

from balder.registry import get_registry

logger = logging.getLogger(__name__)


BALDER_SETTINGS_FIELD = "BALDER_SETTINGS"

SUBSCRIPTION = "SUBSCRIPTION"
QUERY = "QUERY"
MUTATION = "MUTATION"

class BalderRegisterException(Exception):
    pass

class BalderRegisterConfigurationError(BalderRegisterException):
    pass


class BalderObjectWrapper(object):
    object_type = None
    resolver = None
    aslist = False
    asfield = False


class BalderSettings(object):
    enforce_catalog = False
    enforce_registry = False
    provider = "default"
    settingsField = BALDER_SETTINGS_FIELD

    def __init__(self, **kwargs):
        if self.settingsField is None or self.provider is None:
            raise NotImplementedError("Please Provide provider and settingsField in your Baldersettings subclass")
        #Set Defaults from config
        if hasattr(settings, self.settingsField):
            providers = getattr(settings,self.settingsField)
            if self.provider in providers:
                for key, value in providers[self.provider].items():
                    logger.info(f"Overwriting {key} with {value} at {self.provider} in {self.settingsField}")
                    setattr(self,key,value)




class BalderRegister(object):
    type = None
    persistent = False
    provider = None # Should be a string of the backend
    settingsClass = BalderSettings

    def __init__(self, path: str, resolver = None, **kwargs):
        """
        """
        if self.type is None :
            raise BalderRegisterConfigurationError("Specify a Type in your register Function [QUERY, SUBSCRIPTION, MUTATION]")
        if resolver is not None and not callable(resolver):
            raise BalderRegisterConfigurationError("The Resolver you called is not callable")
        self.path = path
        self.kwargs = kwargs


    def __call__(self, cls):
        if issubclass(cls, DjangoObjectType):
            assert self.type == QUERY
            if "aslist" in self.kwargs:
                logger.info(f"Registering {cls.__name__} as ListQuery")
                get_registry().setQueryField("all_jobs", graphene.List(cls, resolver=self.resolver))

        description = self.kwargs.pop("description") if "description" in self.kwargs else None
        if issubclass(cls, BalderObjectWrapper):
            if cls.object_type is None: raise BalderRegisterConfigurationError(f"Please specify a type in your ObjectWrapper {cls.__name__}")
            
            if self.type == QUERY:
                if cls.resolver is None or not callable(cls.resolver): raise BalderRegisterConfigurationError(f"Please specify a callable resolver in your ObjectWrapper {cls.__name__}")
                assert issubclass(cls.object_type, DjangoObjectType)
                if cls.aslist or "aslist" in self.kwargs:
                    logger.info(f"Registering {cls.object_type.__name__} as ListQuery")
                    get_registry().setQueryField(self.path, graphene.List(cls.object_type, description=description, resolver=cls.resolver, **self.kwargs))
                elif cls.asfield or "asfield" in self.kwargs:
                    logger.info(f"Registering {cls.object_type.__name__} as ListQuery")
                    get_registry().setQueryField(self.path, graphene.Field(cls.object_type, description=description, resolver=cls.resolver, **self.kwargs))

            elif self.type == SUBSCRIPTION: 
                assert issubclass(cls.object_type, Subscription)
                logger.info(f"Registering {cls.object_type.__name__} as Subscription")
                get_registry().setSubscriptionField(self.path, cls.object_type.Field())
                get_registry().setSubscription(self.path, cls.object_type)

            else:
                return BalderRegisterConfigurationError(f"Not sure how to register the Subclass of BalderObjectWrapper: {cls.__name__}")


        else:
            raise BalderRegisterConfigurationError(f"Not sure how to register {cls.__name__}")

        return cls


        

class register_subscription(BalderRegister):
    type = SUBSCRIPTION

class register_query(BalderRegister):
    type = QUERY

class register_mutation(BalderRegister):
    type = MUTATION