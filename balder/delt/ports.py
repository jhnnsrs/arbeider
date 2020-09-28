from konfig.widgets import CharWidget, FileWidget, IntWidget, ListWidget, ModelWidget, ObjectWidget, QueryWidget, SliderWidget, SwitchWidget, UUIDWidget
import graphene
from graphene.types.generic import GenericScalar


class WidgetType(graphene.Interface):
    type = graphene.String()
    dependencies = graphene.List(graphene.String, description="The set-keys this widget depends on, check *query parameters*")

    @classmethod
    def resolve_type(cls, instance, info):
        typemap = {
            SliderWidget.type: SliderWidgetType,
            ModelWidget.type: ModelWidgetType,
            CharWidget.type: CharWidgetType,
            SwitchWidget.type: SwitchWidgetType,
            ObjectWidget.type: ObjectWidgetType,
            IntWidget.type: IntWidgetType,
            FileWidget.type: FileWidgetType,
            ListWidget.type: ListWidgetType,
            UUIDWidget.type: UUIDWidgetType,
            QueryWidget.type: QueryWidgetType,
            
        }
        _type = instance.get("type")
        return typemap.get(_type, FakeWidgetType)


class FakeWidgetType(graphene.ObjectType):

    class Meta:
        interfaces = (WidgetType,)

TYPEMAP = {
    str: graphene.String(),
    int: graphene.Int()
}  

def createWidgetType(cls):
    fieldmap = cls().types()
    fieldmap.pop("type")

    fields = {key: TYPEMAP[value] for key, value in fieldmap.items()}

      

    Meta = type("Meta", (object,), { "interfaces" : (WidgetType,)})    
    return type(f"{cls.__name__}Type", (graphene.ObjectType,), { "Meta": Meta, **fields
    })

SliderWidgetType = createWidgetType(SliderWidget)
IntWidgetType = createWidgetType(IntWidget)
ModelWidgetType = createWidgetType(ModelWidget)
CharWidgetType = createWidgetType(CharWidget)
SwitchWidgetType = createWidgetType(SwitchWidget)
QueryWidgetType = createWidgetType(QueryWidget)
UUIDWidgetType = createWidgetType(UUIDWidget)
ListWidgetType = createWidgetType(ListWidget)
FileWidgetType = createWidgetType(FileWidget)
ObjectWidgetType = createWidgetType(ObjectWidget)



class PortType(graphene.Interface):
    key = graphene.String()
    name = graphene.String()
    description = graphene.String(required=False)
    required = graphene.Boolean(required=True)
    primary = graphene.Boolean(required=True, description="Is this the primary driver for this Node?")
    widget = graphene.Field(WidgetType,description="Description of the Widget")

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
    default = graphene.Int()

    class Meta:
        interfaces = (PortType, )

class BoolPortType(graphene.ObjectType):
    default = graphene.Boolean()

    class Meta:
        interfaces = (PortType, )

class CharPortType(graphene.ObjectType):
    default = graphene.String()

    class Meta:
        interfaces = (PortType, )

class FilePortType(graphene.ObjectType):
    default = graphene.String()
    class Meta:
        interfaces = (PortType, )

class ListPortType(graphene.ObjectType):
    default = graphene.List(graphene.String)
    class Meta:
        interfaces = (PortType, )

class UUIDPortType(graphene.ObjectType):
    default = graphene.String()
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

