import hashlib
import inspect
import json
import logging
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import fields, serializers

from delt.discover import (NotDiscoveringError, getCatalog, getDiscover,
                           getRegister)
from delt.exceptions import DeltConfigError
from delt.models import (Node,models)
from delt.node import node_identifier, NodeConfig
from delt.register import BaseRegister, BaseRegisterConfigurationError, BaseRegisterSettings
from delt.registry import get_registry
from delt.discover import NODE_BACKENDS_FIELD, NODEBACKEND_TYPE
logger = logging.getLogger(__name__)
INPUT_IDENTIFIER = "inputs"
OUTPUT_IDENTIFIER = "outputs"
NODE_BACKEND_SETTINGS_FIELD = "NODE_BACKENDS"

class NodeBackendRegisterConfigurationError(BaseRegisterConfigurationError):
    pass


def parse_port(elements: list):
    ports = []
    for el in elements:
        if isinstance(el, dict):
            if "model" not in el: raise DeltConfigError("Your dict does not Provide a model")
            ports.append( el)
        elif isinstance(el, str):
            ports.append({
                "name": el,
                "model": str(el).lower(),
                "map": str(el).lower()
            })
        elif issubclass(el, object):
            ports.append({
                "name": el.__name__,
                "model": str(el.__name__).lower(),
                "map": str(el.__name__).lower()
            })
        else:
            raise DeltConfigError(f"Unknown Port Type {el}")
    return ports

def field_name(field, key):
    item = field.label or field.field_name or key
    print(item)
    return str(item)


def generatePort(key, field , depth=0):
    """Serialized a Key, Field combination to NodePorts, recursively
    
    Arguments:
        key {[str]} -- The key of the field
        field {[serializers.Field]} -- The serializers Field that should be serialized
    Keyword Arguments:
        depth {int} -- [The depth of the Recursion (shouldnt be )] (default: {0})
    
    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
    
    Returns:
        [dict] -- The NodePort dict
    """
    if depth == 3: raise NotImplementedError("Please do not Nest Serializers in a depth bigger then 3")
    try:
        if issubclass(field.default, fields.empty): # Raises exception if not Class
            default = None
        else:
            default = field.default
    except:
        default = field.default

    
    port = {
        "name": field_name(field,key),
        "key": key,
        "description": field.help_text,
        "required": field.required,
        "default": default
    }


    if isinstance(field, serializers.BooleanField):
        return {**port, "type": "bool"}
    elif isinstance(field, serializers.IntegerField):
        return {**port, "type": "int"}
    elif isinstance(field, serializers.CharField):
        return {**port, "type": "char"}

    # Advanced Types
    elif isinstance(field, serializers.PrimaryKeyRelatedField):
        return {**port, "type": "model", "identifier": field.queryset.model.__name__}
    elif isinstance(field, serializers.Serializer):
        argsfields = field.fields #We are dealing with an Instance
        subports = []
        for subkey, subfield in argsfields.items():
            subports.append(generatePort(subkey, subfield, depth=depth+1))
        return {**port, "type": "object", "identifier": field.__class__.__name__, "ports": subports}
    else:
        raise NotImplementedError(f"We dont know how to serialize the {key}: {field}")


def parse_inputs(config: NodeConfig):
    ports = []
    if hasattr(config, INPUT_IDENTIFIER):
        inputs = getattr(config, INPUT_IDENTIFIER)
        argsfields = inputs._declared_fields #We are dealing with an Instance (fields is not accessible)
        for key, field in argsfields.items():
            port = generatePort(key,field)
            ports.append(port)
    return ports

def parse_outputs(config: NodeConfig):
    ports = []
    if hasattr(config, OUTPUT_IDENTIFIER):
        outputs = getattr(config, OUTPUT_IDENTIFIER)
        argsfields = outputs._declared_fields #We are dealing with an Instance (fields is not accessible)
        for key, field in argsfields.items():
            port = generatePort(key,field)
            ports.append(port)
    return ports



class NodeBackendSettings(BaseRegisterSettings):
    enforce_catalog = False
    enforce_registry = False
    provider = None
    settingsField = NODE_BACKENDS_FIELD



class NodeBackendRegister(BaseRegister):
    type = NODEBACKEND_TYPE
    register: Node = None # Should be class of Model
    provider = None # Should be a string of the backend
    settingsClass = NodeBackendSettings

    def __init__(self, config: NodeConfig):
        if not issubclass(self.register, Node):
            raise NodeBackendRegisterConfigurationError(f"Your Register ist not subclassing Node! Its an instance of {self.register.__class__}")
        super().__init__(config)
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

    def get_default_nodetype(self):
        raise NotImplementedError("Please specifiy a default Nodetype to Return")

    def get_node_identifier(self):
        # Will help to identifiy the Node within the Framework
        if self._nodeidentifier is None:
            package = self.get_value_in_derived("package")
            interface = self.get_value_in_derived("interface")
            backend = self.get_value_in_derived("provider")

            self._nodeidentifier = node_identifier(package, interface, backend)
            # The Indentifier should be unique for each
        return self._nodeidentifier


    def catalog_class(self, cls,**kwargs):
        """Implement your Custom Cataloginc Logic Here
        Hint: 
            You should consider using the get_additional_uniques and get_additional_kwargs and setting
            Register, 
        Arguments:
            cls {class} -- The Class that is to be catalgoed
        """
        logger.info(f"Evaluating {cls.__name__}")

        # The Register as a Subclass of Node
        register: Node =  self.get_value_in_derived("register")

        # Will help to identifiy the Node within the Framework
        package = self.get_value_in_derived("package")
        interface = self.get_value_in_derived("interface")
        backend = self.get_value_in_derived("provider")

        # The Indentifier should be unique for each
        identifier = self.get_node_identifier()

        # General
        name = self.get_value_in_derived("name", default=cls.__name__)
        description = self.get_value_in_derived("description", default=cls.__doc__ or "No Description")

        # Graph Related
        inputs = parse_inputs(self.config)
        outputs = parse_outputs(self.config)
        nodeclass = self.get_value_in_derived("nodeclass", default=self.get_default_nodetype())
        variety = self.get_value_in_derived("variety")


        nodeDefaults = {
            "package" : package,
            "interface" : interface,
            "backend" : backend,
            "name":  name,
            "description" : description,
            "inputs" : inputs,
            "outputs" : outputs,
            "nodeclass" : nodeclass,
            "variety" : variety,
        }

        nodeUniques = {
            "identifier" : identifier,

        }

        additionalKwargs = self.get_additional_kwargs()
        additionalUniques = self.get_additional_uniques()

        nodeDefaults.update(additionalKwargs)
        nodeUniques.update(additionalUniques)


        # Register With Backend if channel and node
        if issubclass(self.config, NodeConfig): # A Check
            logger.info(f"Registering {cls.__name__} wtih {register.__name__}")
            try:
                node = register.objects.get(**nodeUniques)
                for key, value in nodeDefaults.items():
                    setattr(node, key, value)
                node.save()
                logger.info(f"Updated {package}/{interface} on Identifier: {identifier}")
            except ObjectDoesNotExist:
                combined = {**nodeUniques}
                combined.update(nodeDefaults)
                node = register(**combined)
                node.save()
                logger.info(f"Created {package}/{interface} on Identifier: {identifier}")
            logger.info("Registered succesfully")
        
        else:
            raise NotImplementedError(f"Not Sure how to register {cls.__name__}")

        return node

    def get_settings(self):
        if self._settings is None:
            self._settings = self.settingsClass()
        return self._settings

