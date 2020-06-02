import logging
import re

import django
import graphene
from django.utils.html import strip_tags
from graphene.types.generic import GenericScalar
from graphene_django.registry import get_global_registry
from rest_framework import fields, serializers

logger = logging.getLogger(__name__)

class GenerationError(Exception):
    pass

def generate_type_name(path):
    return re.sub(r"[^A-Za-z]+", '', path.capitalize())

def generateGrapheneField(key, field: fields.Field , depth=0, args=False, prefix=""):
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
    serializerField = graphene.Field
    serializerType = graphene.ObjectType
    if args:
        serializerField = graphene.Argument
        serializerType = graphene.InputObjectType

    if depth == 3: raise NotImplementedError("Please do not Nest Serializers in a depth bigger then 3")
    try:
        if issubclass(field.default, fields.empty): # Raises exception if not Class
            default = None
        else:
            default = field.default
    except:
        default = field.default

    required = field.required
    description = strip_tags(field.help_text)
    print(description)

    if isinstance(field, serializers.BooleanField):
        return {key: graphene.Boolean(required=required, description=description)}
    elif isinstance(field, serializers.IntegerField):
        return {key: graphene.Int(required=required, description=description)}
    elif isinstance(field, serializers.CharField):
        return {key: graphene.String(required=required, description=description)}
    elif isinstance(field, serializers.FloatField):
        return {key: graphene.Float(required=required, description=description)}
    elif isinstance(field, serializers.UUIDField):
        return {key: graphene.UUID(required=required, description=description)}
    elif isinstance(field, serializers.ListField):
        child = generateGrapheneField("key", field.child, depth=depth+1, args=input)
        return {key: graphene.List(child["key"].__class__, required=required, description=description)}
    elif isinstance(field, serializers.JSONField):
        return {key: GenericScalar(required=required, description=description)}
    elif isinstance(field, serializers.PrimaryKeyRelatedField):
        if args:
            return {key: graphene.ID(required=required, description=description)}
        else:
            modeltype = get_global_registry().get_type_for_model(field.queryset.model)
            if modeltype is None:
                raise GenerationError(f"There is no GrapheneType registered for Model {field.queryset.model.__name__}")
            return {key: graphene.Field(modeltype, required=required, description=description)}
    elif isinstance(field, serializers.Serializer) and not isinstance(field, serializers.ModelSerializer):
        argsfields = field.fields #We are dealing with an Instance
        subports = {}
        for subkey, subfield in argsfields.items():
            subports.update(generateGrapheneField(subkey, subfield, depth=depth+1, args=input))
        return {key: serializerField(type(prefix + field.__class__.__name__, (serializerType,), {**subports, "__doc__": field.__class__.__doc__}),)}
    elif isinstance(field, serializers.ModelSerializer):
        modeltype = get_global_registry().get_type_for_model(field.Meta.model)
        if modeltype is None:
            raise GenerationError(f"There is no GrapheneType registered for Model {field.Meta.model.__name__}")
        return {key: serializerField(modeltype, required=required, description=description)}
    else:
        logger.error(f"No idea how to parse this {field}")
        raise Exception("No idea what")

def generate_grapheneargs_from_serializer(serializer):
    ports = {}
    argsfields = serializer.fields.fields #We are dealing with an Instance (delclared_fields is not accessible)
    for key, field in argsfields.items():
        port = generateGrapheneField(key,field, args= True, prefix="")
        ports.update(port)
    return ports
    
def generate_graphenefields_from_serializer(serializer):
    ports = {}
    argsfields = serializer.fields.fields #We are dealing with an Instance (delclared_fields is not accessible)
    for key, field in argsfields.items():
        port = generateGrapheneField(key,field, prefix="")
        ports.update(port)
    return ports


def generateArgumentsFromGrapheneFields(name, fields, description="These are generic Arguments"):
    genericFields = {
         "__doc__": f"{description}"
    }
    print("THE ARGUMENTS", fields)
    return type(name+"Arguments", (object,),{ **genericFields, **fields})
