from rest_framework import fields, serializers

from delt.nodes.base import NodeBackendRegisterConfigurationError
from delt.models import Node
from konfig.node import Konfig

INPUT_IDENTIFIER = "inputs"
OUTPUT_IDENTIFIER = "outputs"
NODE_BACKEND_SETTINGS_FIELD = "NODE_BACKENDS"

class KonfigParsingError(NodeBackendRegisterConfigurationError):
    pass

def parse_port(elements: list):
    ports = []
    for el in elements:
        if isinstance(el, dict):
            if "model" not in el: raise KonfigParsingError("Your dict does not Provide a model")
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
            raise KonfigParsingError(f"Unknown Port Type {el}")
    return ports

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
    elif isinstance(field, serializers.FileField):
        return {**port, "type": "file"}
    elif isinstance(field, serializers.ListField):
        return {**port, "type": "list"}
    elif isinstance(field, serializers.UUIDField):
        return {**port, "type": "uuid"}

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
