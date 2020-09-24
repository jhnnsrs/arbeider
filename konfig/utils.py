from herre.fields import FileField
from rest_framework import fields, serializers

from delt.nodes.base import NodeBackendRegisterConfigurationError
from delt.models import Node
from konfig.node import Konfig
from konfig.params import *

INPUT_IDENTIFIER = "inputs"
OUTPUT_IDENTIFIER = "outputs"
NODE_BACKEND_SETTINGS_FIELD = "NODE_BACKENDS"

class KonfigParsingError(NodeBackendRegisterConfigurationError):
    pass

def field_name(field, key):
    item = field.label or field.field_name or key
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

    if isinstance(field, PortMixin):
        # Port Mixins can generate themselves Dynamically
        return field.build_port(key)
    elif isinstance(field, serializers.Serializer):
        argsfields = field.fields #We are dealing with an Instance
        subports = []
        for subkey, subfield in argsfields.items():
            subports.append(generatePort(subkey, subfield, depth=depth+1))
        return { "name": field_name(field,key),
        "key": key,
        "description": field.help_text,
        "required": field.required, "default": None, "type": "object", "identifier": field.__class__.__name__, "ports": subports}
    else:
        raise NotImplementedError(f"We dont know how to serialize the {key}: {field}")


def parse_inputs(config: Konfig):
    ports = []
    if hasattr(config, INPUT_IDENTIFIER):
        inputs = getattr(config, INPUT_IDENTIFIER)
        argsfields = inputs._declared_fields #We are dealing with an Instance (fields is not accessible)
        for key, field in argsfields.items():
            port = generatePort(key,field)
            ports.append(port)
    return ports

def parse_outputs(config: Konfig):
    ports = []
    if hasattr(config, OUTPUT_IDENTIFIER):
        outputs = getattr(config, OUTPUT_IDENTIFIER)
        argsfields = outputs._declared_fields #We are dealing with an Instance (fields is not accessible)
        for key, field in argsfields.items():
            port = generatePort(key,field)
            ports.append(port)
    return ports
