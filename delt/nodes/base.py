import hashlib
import inspect
import json
import logging
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import fields, serializers

from delt.discover import (NODE_BACKEND_TYPE, NODE_BACKENDS_FIELD,
                           NotDiscoveringError, getCatalog, getDiscover,
                           getRegister)
from delt.exceptions import DeltConfigError
from delt.models import Node
from delt.register import (BaseRegister, BaseRegisterConfigurationError,
                           BaseRegisterSettings)

logger = logging.getLogger(__name__)

DEFAULT_JOB_PUBLISHERS = settings.DEFAULT_JOB_PUBLISHERS if hasattr(settings, "DEFAULT_JOB_PUBLISHERS") else []
DEFAULT_PUBLISHERS = settings.DEFAULT_PUBLISHERS if hasattr(settings, "DEFAULT_PUBLISHERS") else { "job": DEFAULT_JOB_PUBLISHERS }
INPUT_IDENTIFIER = "inputs"
OUTPUT_IDENTIFIER = "outputs"
NODE_BACKEND_SETTINGS_FIELD = "NODE_BACKENDS"

class NodeBackendRegisterConfigurationError(BaseRegisterConfigurationError):
    pass


class NodeBackendSettings(BaseRegisterSettings):
    enforce_catalog = False
    enforce_registry = False
    provider = None
    settingsField = NODE_BACKENDS_FIELD
    defaultPublishers = DEFAULT_PUBLISHERS



class NodeBackendRegister(BaseRegister):
    type = NODE_BACKEND_TYPE
    register: Node = None # Should be class of Model
    provider = None # The Provider translated to the Realm instance
    settings: NodeBackendSettings = None

    def __init__(self, **kwargs):
        if not issubclass(self.register, Node):
            raise NodeBackendRegisterConfigurationError(f"Your Register ist not subclassing Node! Its an instance of {self.register.__class__}")
        if not isinstance(self.settings, NodeBackendSettings):
            raise NodeBackendRegisterConfigurationError(f"Your Settings ist not an Instance of NodeBackendSettings or its subclass! Its an instance of {self.register.__class__}")
        
        super().__init__(**kwargs)
        self._nodeidentifier = None
