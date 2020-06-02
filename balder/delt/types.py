import graphene
from graphene.types.generic import GenericScalar


class BasePortType(graphene.ObjectType):
    key = graphene.String()
    name = graphene.String()
    default = graphene.String(required=False)
    description = graphene.String(required=False)
    required = graphene.Boolean(required=True)


class IntPortType(BasePortType):
    pass

class BoolPortType(BasePortType):
    pass

class CharPortType(BasePortType):
    pass

class IntPortType(BasePortType):
    pass

class FilePortType(BasePortType):
    pass

class ListPortType(BasePortType):
    pass

class UUIDPortType(BasePortType):
    pass

# Advanced Types according to nodes/base
class ObjectPortType(BasePortType):
    ports = graphene.List(lambda: PortType)
    identifier = graphene.String()


class ModelPortType(BasePortType):
    identifier = graphene.String()


class PortType(graphene.Union):
    
    class Meta:
        types = (
            BoolPortType,
            CharPortType,
            IntPortType,
            FilePortType,
            ListPortType,
            UUIDPortType,
            ModelPortType,
            ObjectPortType, 
            BasePortType
            )

    @classmethod
    def resolve_type(cls, instance, info):
        typemap = {
            "int": IntPortType,
            "bool": BoolPortType,
            "char": CharPortType,
            "file": FilePortType,
            "list": ListPortType,
            "uuid": UUIDPortType,
            "object": ObjectPortType,
            "model": ModelPortType,
        }
        _type = instance.pop("type")
        return typemap.get(_type, BasePortType)
