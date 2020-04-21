import hashlib
import inspect
import json
import logging
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import fields, serializers

from delt.discover import (POD_BACKEND_TYPE, POD_BACKENDS_FIELD,
                           NotDiscoveringError, getCatalog, getDiscover,
                           getRegister)
from delt.exceptions import DeltConfigError
from delt.models import Node, Pod, models
from delt.node import NodeConfig, node_identifier
from delt.pod import pod_identifier
from delt.register import (BaseRegister, BaseRegisterConfigurationError,
                           BaseRegisterSettings)
from delt.registry import get_registry

logger = logging.getLogger(__name__)
INPUT_IDENTIFIER = "inputs"
OUTPUT_IDENTIFIER = "outputs"
NODE_BACKEND_SETTINGS_FIELD = "NODE_BACKENDS"

class PodBackendRegisterConfigurationError(BaseRegisterConfigurationError):
    pass


class NodeNotFoundError(PodBackendRegisterConfigurationError):
    pass




class PodBackendSettings(BaseRegisterSettings):
    enforce_catalog = False
    enforce_registry = False
    provider = None
    settingsField = POD_BACKENDS_FIELD



class PodBackendRegister(BaseRegister):
    type = POD_BACKEND_TYPE
    persistent = False
    register: Pod = None # Should be class of Model
    provider = None # Should be a string of the backend
    settingsClass = PodBackendSettings

    def __init__(self, config: NodeConfig):
        if not issubclass(self.register, Pod):
            raise PodBackendRegisterConfigurationError(f"Your Register ist not subclassing Pod! Its an instance of {self.register.__class__}")
        super().__init__(config)
        self._podidentifier = None
        self._nodeidentifier = None

    def get_additional_kwargs(self):
        """Should return additional Kwargs for the Model Creation (Reference should be the Register you are trying to register with)
        
        Returns:
            [dict] -- The additional Kwargs
        """
        return {}
            
    def get_additional_uniques(self):
        """Should return additional Kwargs for the Model Creation (Reference should be the Register you are trying to register with)
        
        Returns:
            [dict] -- The additional Kwargs
        """
        return {}

    def get_default_podclass(self):
        raise NotImplementedError("Please specifiy a default Nodetype to Return")

    def get_node_identifier(self):
        # Will help to identifiy the Node within the Framework
        if self._nodeidentifier is None:
            package = self.get_value_in_derived("package")
            interface = self.get_value_in_derived("interface")

            self._nodeidentifier = node_identifier(package, interface)
            # The Indentifier should be unique for each
        return self._nodeidentifier

    def get_pod_identifier(self):
        # Will help to identifiy the Node within the Framework
        if self._podidentifier is None:
            package = self.get_value_in_derived("package")
            interface = self.get_value_in_derived("interface")
            provider = self.get_value_in_derived("provider")

            self._podidentifier = pod_identifier(package, interface, provider)
            # The Indentifier should be unique for each
        return self._podidentifier

    def get_node_by_identifier(self):
        identifier = self.get_node_identifier()
        try:
            return Node.objects.get(identifier = identifier)
        except Node.DoesNotExist as e:
            raise NodeNotFoundError(f"Node for Pod not found: Searched for {identifier}")

    def catalog_class(self, cls,**kwargs):
        """Implement your Custom Cataloginc Logic Here
        Hint: 
            You should consider using the get_additional_uniques and get_additional_kwargs and setting
            Register, 
        Arguments:
            cls {class} -- The Class that is to be catalgoed
        """
        logger.info(f"Adding {cls.__name__} to Pods")


        node = self.get_node_by_identifier()
        # The Register as a Subclass of Node

        register: Pod =  self.get_value_in_derived("register")
        # Will help to identifiy the Node within the Framework

        persistent = self.get_value_in_derived("persistent")
        provider = self.get_value_in_derived("provider")
        podclass = self.get_value_in_derived("podclass", default=self.get_default_podclass())
        print(persistent)

        nodeDefaults = {
            "node" : node,
            "persistent":  persistent,
            "podclass" : podclass,
            "provider" : provider,
        }

        nodeUniques = {

        }

        additionalKwargs = self.get_additional_kwargs()
        additionalUniques = self.get_additional_uniques()

        nodeDefaults.update(additionalKwargs)
        nodeUniques.update(additionalUniques)

        if not bool(nodeUniques):
            raise PodBackendRegisterConfigurationError("Please provided at least one unique identifier if you register through this backend")
        # Register With Backend if channel and node
        if issubclass(self.config, NodeConfig): # A Check
            logger.info(f"Registering {cls.__name__} wtih {register.__name__}")
            try:
                pod = register.objects.get(**nodeUniques)
                for key, value in nodeDefaults.items():
                    setattr(pod, key, value)
                pod.save()
                logger.info(f"Updated Pod on Node {node.name}")
            except ObjectDoesNotExist:
                combined = {**nodeUniques}
                combined.update(nodeDefaults)
                pod = register(**combined)
                pod.save()
                logger.info(f"Created Pod on Node {node.name}")
            logger.info("Registered succesfully")
        
        else:
            raise NotImplementedError(f"Not Sure how to register {cls.__name__}")

        return pod

    def get_settings(self):
        if self._settings is None:
            self._settings = self.settingsClass()
        return self._settings
