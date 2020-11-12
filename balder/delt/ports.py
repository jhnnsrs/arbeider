from typing import List
from konfig.widgets import Widget, CharWidget, FileWidget, IntWidget, ListWidget, ModelWidget, ObjectWidget, QueryWidget, SliderQueryWidget, SliderWidget, SwitchWidget, UUIDWidget
from konfig.params import ModelPort, ObjectPort, IntPort, CharPort, FloatPort, FilePort, BoolPort, ListPort, PortMixin, UUIDPort

import graphene
from graphene.types.generic import GenericScalar



get_widget_types = lambda: {
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
    SliderQueryWidget.type: SliderQueryWidgetType,
}


get_port_types = lambda: {
            IntPort.type: IntPortType,
            BoolPort.type: BoolPortType,
            CharPort.type:  CharPortType,
            FilePort.type: FilePortType,
            ListPort.type:  ListPortType,
            FloatPort.type: FloatPortType,
            UUIDPort.type:  UUIDPortType,
            ObjectPort.type:  ObjectPortType,
            ModelPort.type: ModelPortType,
}






class WidgetType(graphene.Interface):
    type = graphene.String()
    dependencies = graphene.List(graphene.String, description="The set-keys this widget depends on, check *query parameters*")

    @classmethod
    def resolve_type(cls, instance, info):
        typemap = get_widget_types()
        _type = instance.get("type")
        return typemap.get(_type, FakeWidgetType)


class PortType(graphene.Interface):
    key = graphene.String()
    label = graphene.String()
    description = graphene.String(required=False)
    required = graphene.Boolean()
    primary = graphene.Boolean( description="Is this the primary driver for this Node?")
    widget = graphene.Field(WidgetType,description="Description of the Widget")

    @classmethod
    def resolve_type(cls, instance, info):
        typemap = get_port_types()
        _type = instance.pop("type")
        return typemap.get(_type, PortType)


class FakeWidgetType(graphene.ObjectType):

    class Meta:
        interfaces = (WidgetType,)

TYPEMAP = {
    str: graphene.String(),
    int: graphene.Int(),
    float: graphene.Float(),
    bool: graphene.Boolean(),
    Widget: WidgetType,
    List[str]: graphene.List(graphene.String), 
    List[PortMixin]: graphene.List(lambda: PortType)
}  

def createWidgetType(cls):
    instance = cls()
    fieldmap = instance.types()
    fieldmap.pop("type")

    fields = {key: TYPEMAP[value] for key, value in fieldmap.items()}

      

    Meta = type("Meta", (object,), { "interfaces" : (WidgetType,)})    
    return type(f"{cls.__name__}Type", (graphene.ObjectType,), { "Meta": Meta, **fields, "__doc__": instance.description, "_label": "nanan"
    })


def createPortType(cls):
    fieldmap = cls.types()
    fieldmap.pop("type")

    fields = {key: TYPEMAP.get(value, GenericScalar) for key, value in fieldmap.items()}

      

    Meta = type("Meta", (object,), { "interfaces" : (PortType,)})    
    return type(f"{cls.__name__}Type", (graphene.ObjectType,), { "Meta": Meta, **fields, "__doc__": cls.description, "_label": "nanan"
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
SliderQueryWidgetType = createWidgetType(SliderQueryWidget)


IntPortType = createPortType(IntPort)
CharPortType = createPortType(CharPort)
BoolPortType = createPortType(BoolPort)
ListPortType = createPortType(ListPort)
FilePortType = createPortType(FilePort)
FloatPortType = createPortType(FloatPort)
UUIDPortType = createPortType(UUIDPort)
ObjectPortType = createPortType(ObjectPort)
ModelPortType = createPortType(ModelPort)




