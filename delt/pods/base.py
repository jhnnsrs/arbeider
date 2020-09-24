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
from delt.pod import pod_identifier
from delt.register import (BaseRegister, BaseRegisterConfigurationError,
                           BaseRegisterSettings)
from delt.registry import get_registry

logger = logging.getLogger(__name__)
INPUT_IDENTIFIER = "inputs"
OUTPUT_IDENTIFIER = "outputs"
NODE_BACKEND_SETTINGS_FIELD = "NODE_BACKENDS"


def pod_identifier(package, interface, provider,  withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    hash = hashlib.sha1()
    salt = package + interface + provider + withsecret
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()

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

    def __init__(self, node: Node, **kwargs):
        if not issubclass(self.register, Pod):
            raise PodBackendRegisterConfigurationError(f"Your Register ist not subclassing Pod! Its an instance of {self.register.__class__}")
        if not isinstance(node, Node):
            raise PodBackendRegisterConfigurationError(f"You have not provided the right Node you provided {str(node)}")
        self._podidentifier = None
        self._node = node
        self._kwargs = kwargs
        super(PodBackendRegister,self).__init__(**kwargs)

    def get_default_podclass(self):
        raise NotImplementedError("Please specifiy a default Nodetype to Return")

    def get_node_identifier(self):
        # Will help to identifiy the Node within the Framework
        return self._node.get_identifier()

    def get_pod_identifier(self):
        # Will help to identifiy the Pod within the Framework
        if self._podidentifier is None:
            self._podidentifier = pod_identifier(self._node.package, self._node.interface, self.provider)
            # The Indentifier should be unique for each
        return self._podidentifier


