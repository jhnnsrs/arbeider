import hashlib
import inspect
import json
import logging
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from delt.models import Node, Route
from delt.node import NodeConfig
from delt.register import BaseRegister, BaseRegisterConfigurationError
from delt.registry import get_registry
from delt.discover import ROUTER_TYPE, ROUTER_BACKENDS_FIELD


logger = logging.getLogger(__name__)

class RouterRegistryConfigurationError(BaseRegisterConfigurationError):
    pass


def route_identifier(package, interface, backend, withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    hash = hashlib.sha1()
    salt = package + interface + backend + withsecret
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()

class RouterRegisterSettings(RouterRegistryConfigurationError):
    enforce_catalog = False
    enforce_registry = False
    provider = None
    settingsField = ROUTER_BACKENDS_FIELD


class RouterRegister(BaseRegister):
    type = ROUTER_TYPE
    register: Route = None
    config: NodeConfig = None
    provider = None
    settingsClass = None

    def __init__(self, config: NodeConfig):
        if self.register is None or not issubclass(self.register, Route):
            raise RouterRegistryConfigurationError("Please specifiy ")
        super().__init__(config)
        self._routeidentifier = None

    def get_route_identifier(self):
        # Will help to identifiy the Node within the Framework
        if self._routeidentifier is None:
            package = self.get_value_in_derived("package")
            interface = self.get_value_in_derived("interface")
            provider = self.get_value_in_derived("provider")

            self._routeidentifier = route_identifier(package, interface, provider)
        # The Indentifier should be unique for each
        return self._routeidentifier

    def get_additional_kwargs(self):
        return {}

    def get_additional_uniques(self):
        return {}

    def catalog_class(self, cls, **kwargs):
        """Implement your Custom Cataloginc Logic Here
        Hint: 
            You should consider using the get_additional_uniques and get_additional_kwargs and setting
            Register, 
        Arguments:
            cls {class} -- The Class that is to be catalgoed
        """
        logger.info(f"Evaluating {cls.__name__}")

        # The Register as a Subclass of Node
        register: Route =  self.register

        # Will help to identifiy the Node within the Framework
        package = self.get_value_in_derived("package")
        interface = self.get_value_in_derived("interface")
        provider = self.get_value_in_derived("provider")

        # The Indentifier should be unique for each
        identifier = self.get_route_identifier()

        # General
        name = self.get_value_in_derived("name", default=cls.__name__)
        description = self.get_value_in_derived("description", default=cls.__doc__ or "No Description")

        # Graph Related

        routeDefaults = {
            "package" : package,
            "interface" : interface,
            "name":  name,
            "description" : description,
            "provider": provider
        }

        # Node
        # If this route is associated with any Route

        try:
            node = Node.objects.get(package=package, interface=interface)
            routeDefaults["node"] = node
        except Exception as e:
            logger.info(f"No Node found for {cls.__name__}: {e}")

        routeUniques = {
            "identifier" : identifier,

        }

        additionalKwargs = self.get_additional_kwargs()
        additionalUniques = self.get_additional_uniques()

        routeDefaults.update(additionalKwargs)
        routeUniques.update(additionalUniques)


        # Register With Backend if channel and node
        if issubclass(self.config, NodeConfig): # A Check
            logger.info(f"Registering {cls.__name__} wtih {register.__name__}")
            try:
                route = register.objects.get(**routeUniques)
                for key, value in routeDefaults.items():
                    setattr(route, key, value)
                route.save()
                logger.info(f"Updated {package}/{interface} on Identifier: {identifier}")
            except ObjectDoesNotExist:
                combined = {**routeUniques}
                combined.update(routeDefaults)
                route = register(**combined)
                route.save()
                logger.info(f"Created {package}/{interface} on Identifier: {identifier}")
            logger.info("Registered succesfully")
        
        else:
            raise NotImplementedError(f"Not Sure how to register {cls.__name__}")

        return route




class register_route(NodeConfig):
    pass