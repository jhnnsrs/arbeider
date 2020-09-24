import graphene


class PortType(graphene.Interface):
    key = graphene.String()
    name = graphene.String()
    default = graphene.String(required=False)
    description = graphene.String(required=False)
    required = graphene.Boolean(required=True)
    primary = graphene.Boolean(required=True, description="Is this the primary driver for this Node?")

    @classmethod
    def resolve_type(cls, instance, info):
        typemap = {
            "int": IntPortType,
            "bool": BoolPortType,
            "char":  CharPortType,
            "file": FilePortType,
            "list":  ListPortType,
            "uuid":  UUIDPortType,
            "object":  ObjectPortType,
            "model": ModelPortType,
        }
        _type = instance.pop("type")
        return typemap.get(_type, PortType)


class IntPortType(graphene.ObjectType):
    class Meta:
        interfaces = (PortType, )

class BoolPortType(graphene.ObjectType):
   class Meta:
        interfaces = (PortType, )

class CharPortType(graphene.ObjectType):
    class Meta:
        interfaces = (PortType, )
     
class IntPortType(graphene.ObjectType):
    class Meta:
        interfaces = (PortType, )

class FilePortType(graphene.ObjectType):
    class Meta:
        interfaces = (PortType, )

class ListPortType(graphene.ObjectType):
    class Meta:
        interfaces = (PortType, )

class UUIDPortType(graphene.ObjectType):
    class Meta:
        interfaces = (PortType, )

# Advanced Types according to nodes/base
class ObjectPortType(graphene.ObjectType):
    class Meta:
        interfaces = (PortType, )

    ports = graphene.List(lambda: PortType)
    identifier = graphene.String()

class ModelPortType(graphene.ObjectType):
    class Meta:
        interfaces = (PortType, )

    identifier = graphene.String()

