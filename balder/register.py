from delt.bouncers.context import BouncerContext
import logging

import graphene
from channels_graphql_ws import Subscription
from django.conf import settings
from graphene_django import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from jinja2.utils import object_type_repr

from balder.fields import BalderFilterField
from balder.queries.base import BaseQuery
from balder.registry import get_registry
from balder.subscriptions.base import BaseSubscription
from balder.subscriptions.job import BaseJobSubscription
from balder.types import BalderObjectType
from balder.wrappers import (BalderMutationWrapper, BalderObjectWrapper,
                             BalderQueryWrapper, BalderSubscriptionWrapper,
                             BaseSubscriptionWrapper, NodeSubscriptionWrapper)
from delt.node import NodeConfig

logger = logging.getLogger(__name__)


BALDER_SETTINGS_FIELD = "BALDER_SETTINGS"

SUBSCRIPTION = "SUBSCRIPTION"
QUERY = "QUERY"
MUTATION = "MUTATION"

class BalderRegisterException(Exception):
    pass

class BalderRegisterConfigurationError(BalderRegisterException):
    pass


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



def bounced_root_info(resolver):
    ''' Replaced the info object with a bounced context object'''
    def bounced(root, info, *args, **kwargs):
        context = BouncerContext(info=info)
        return resolver(root, context, *args, **kwargs)

    return bounced



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
        description = self.kwargs.pop("description") if "description" in self.kwargs else None
        aslist = self.kwargs.pop("aslist") if "aslist" in self.kwargs else False
        withfilter = self.kwargs.pop("withfilter") if "withfilter" in self.kwargs else False
        asfield = self.kwargs.pop("asfield") if "asfield" in self.kwargs else False
        
        if self.type == QUERY:
            if issubclass(cls, BalderObjectWrapper):
                if cls.object_type is None: raise BalderRegisterConfigurationError(f"Please specify a type in your ObjectWrapper {cls.__name__}")
                if cls.resolver is None or not callable(cls.resolver): raise BalderRegisterConfigurationError(f"Please specify a callable resolver in your ObjectWrapper {cls.__name__}")
                assert issubclass(cls.object_type, BalderObjectType)
                if cls.aslist or aslist:
                    if cls.withfilter or withfilter:
                        logger.info(f"Registering {cls.object_type.__name__} as ListQuery with DjangoFilter")
                        get_registry().setQueryField(self.path, BalderFilterField(cls.object_type, description=description, **self.kwargs))
                    else:
                        logger.info(f"Registering {cls.object_type.__name__} as ListQuery")
                        get_registry().setQueryField(self.path, graphene.List(cls.object_type, description=description, resolver=bounced_root_info(cls.resolver), **self.kwargs))
                elif cls.asfield or asfield:
                    logger.info(f"Registering {cls.object_type.__name__} as ListQuery")
                    get_registry().setQueryField(self.path, graphene.Field(cls.object_type, description=description, resolver=bounced_root_info(cls.resolver), **self.kwargs))
                else:
                    raise BalderRegisterConfigurationError(f"Not sure how to register the Subclass of BalderObjectWrapper: {cls.__name__} no asfield or aslist argument Provided")
            elif issubclass(cls, BalderQueryWrapper):
                wrapperinstance = cls(self.path)
                object_type = wrapperinstance.get_object()
                if issubclass(object_type, BaseQuery):
                    wrapperinstance = cls(self.path)
                    object_type = wrapperinstance.get_object()
                    get_registry().setQueryField(self.path, object_type.Field())
            else:
                raise BalderRegisterConfigurationError(f"Not sure how to register the Query {cls.__name__}, as it is not a BalderObjectWrapper")

        elif self.type == SUBSCRIPTION: 
            if issubclass(cls, BaseSubscriptionWrapper):
                wrapperinstance = cls(self.path)
                object_type = wrapperinstance.get_object()
                if issubclass(object_type, BaseJobSubscription):
                    config: NodeConfig = cls.config
                    object_type.config = config
                    get_registry().setSubscriptionField(self.path, object_type.Field(description=cls.config.__doc__))
                    get_registry().setSubscriptionForNode(config.get_node(), object_type)
                    logger.info(f"Registering {object_type.__name__} as JobSubscription")
                elif issubclass(object_type, BaseSubscription):
                    wrapperinstance = cls(self.path)
                    object_type = wrapperinstance.get_object()
                    get_registry().setSubscriptionField(self.path, object_type.Field())
                else:
                    raise BalderRegisterConfigurationError(f"Not sure how to register subscription {cls.__name__}. {object_type.__name__} does not inherit from BaseSubscription")
            else:
                raise BalderRegisterConfigurationError(f"Not sure how to Subscription: {cls.__name__}, Not Wrapped")
           

        elif self.type == MUTATION: 
            if issubclass(cls, BalderMutationWrapper):
                wrapperinstance = cls(self.path)
                object_type = wrapperinstance.get_object()
                logger.info(f"Registering {object_type.__name__} as Mutation")
                get_registry().setMutationField(self.path, object_type.Field())
            else:
                raise BalderRegisterConfigurationError(f"Not sure how to Mutation: {cls.__name__}, Not Wrapped")

            
        else:
            raise BalderRegisterConfigurationError(f"Not sure how to register {cls.__name__}")

        return cls


        

class register_subscription(BalderRegister):
    type = SUBSCRIPTION

class register_query(BalderRegister):
    type = QUERY

class register_mutation(BalderRegister):
    type = MUTATION