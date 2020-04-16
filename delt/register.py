import inspect
import logging

from django.conf import settings

from delt.discover import (NotDiscoveringError, getCatalog, getDiscover,
                           getRegister)
from delt.node import NodeConfig

logger = logging.getLogger(__name__)

def props(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not inspect.ismethod(value):
            pr[name] = value
    return pr

class BaseRegisterSettings(object):
    enforce_catalog = False
    enforce_registry = False
    provider = None
    settingsField = None

    def __init__(self, **kwargs):
        if self.settingsField is None or self.provider is None:
            raise NotImplementedError("Please Provide provider and settingsField in your Register Settings")
        #Set Defaults from config
        if hasattr(settings, self.settingsField):
            providers = getattr(settings,self.settingsField)
            if self.provider in providers:
                for key, value in providers[self.provider].items():
                    logger.info(f"Overwriting {key} with {value} at {self.provider} in {self.settingsField}")
                    setattr(self,key,value)

class BaseRegisterConfigurationError(Exception):
    pass

class BaseRegister(object):
    config: NodeConfig = None
    type = None
    provider = None
    settingsClass = None

    def __init__(self, config: NodeConfig):
        if not getDiscover(): raise NotDiscoveringError("This module was called while not Discovering. Please make sure it is not imported")
        if not issubclass(config, NodeConfig):
            raise BaseRegisterConfigurationError(f"You didnt provide a Proper NodeConfig in {self.__name__}")
        if self.type is None:
            raise BaseRegisterConfigurationError(f"Please provided a type property to your BaseRegister")
        if self.provider is None:
            raise BaseRegisterConfigurationError(f"Please provided a provider property to your BaseRegister")
        if self.settingsClass is None:
            raise BaseRegisterConfigurationError(f"Please provided a settingsClass property to your BaseRegister")
       
        # First we introspect the class and config
        self.self_properties = props(self)
        self.config_properties = props(config)

        self.config = config
        self._settings = None


    def get_value_in_derived(self, key, default=None):
        """Searches in ascdening order for overwritten properties 

        Register -> Config -> default

        None elements are ignored and resort to KeyError
        
        Arguments:
            key {str} -- The Property
        
        Keyword Arguments:
            default {bool} -- The default it should resort to if no property is detected (default: {None})
        
        Raises:
            KeyError: If the Property doesnt exist and no default was set
        
        Returns:
            any -- Returns the property
        """
        if key in self.self_properties and self.self_properties[key] is not None:
            return self.self_properties[key]
        elif key in self.config_properties and self.config_properties[key] is not None:
            return self.config_properties[key]
        else:
            if default is not None: return default
            raise KeyError(f" '{key}' does not exist in {self.config.__name__} or {self.__class__.__name__}")

    def get_additional_kwargs(self):
        return {}

    def get_additional_uniques(self):
        return {}

    def catalog_class(self, cls,**kwargs):
        """Implement your Custom Cataloginc Logic Here
        Hint: 
            You should consider using the get_additional_uniques and get_additional_kwargs and setting
            Register, 
        Arguments:
            cls {class} -- The Class that is to be catalgoed
        """
        raise NotImplementedError

    def register_class(self, cls):
        """Implement your Custom Registration Logic Here
        """

    def class_registered(self, cls):
        """ The cataloged class as a Callback

        Arguments:
            cls {class} -- The Class that was registered
        """
        pass

    def class_cataloged(self, cls):
        """ The cataloged class as a Callback
        
        Arguments:
            node {Node} -- The Node as a instance of the Register 
        """
        pass

    def cls_to_be_registered(self, cls):
        """If you want ton adjust some class settings according to your backend here is the plase
        
        Arguments:
            cls {BaseNodeType} -- The class this decorater was called with
        
        Returns:
            [BaseNodeType] -- The altered class
        """
        return cls
    
    def cls_to_be_cataloged(self, cls):
        """If you want ton adjust some class settings according to your backend here is the plase
        
        Arguments:
            cls {BaseNodeType} -- The class this decorater was called with
        
        Returns:
            [BaseNodeType] -- The altered class
        """
        return cls

    def cls_to_be_returned(self, cls):
        """If you want ton adjust some class settings according to your backend here is the plase
        
        Arguments:
            cls {class} -- The class this decorater was called with
        
        Returns:
            [BaseNodeType] -- The altered class
        """
        return cls

    def __call__(self, cls):
        # Do Initial Weird stuff to class


        if getRegister(self.provider, self.type) or self.get_settings().enforce_registry:
            registered = self.register_class(self.cls_to_be_registered(cls))
            self.class_registered(registered)

        if getCatalog(self.provider, self.type) or self.get_settings().enforce_catalog:
            node = self.catalog_class(self.cls_to_be_cataloged(cls))
            self.class_cataloged(node)

        return self.cls_to_be_returned(cls)

    def get_settings(self):
        if self._settings is None and self.settingsClass is not None:
            self._settings = self.settingsClass()
        return self._settings
