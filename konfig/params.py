from konfig.widgets import CharWidget, FloatWidget, IntWidget, ListWidget, ModelWidget, ObjectWidget, SwitchWidget, UUIDWidget, Widget
import logging
import uuid

from rest_framework import fields, serializers
from rest_framework.fields import empty
from rest_framework.relations import PrimaryKeyRelatedField


logger = logging.getLogger(__name__)

class PortMixin(object):
    widget = None
    type = None

    def __init__(self, *args, **kwargs) -> None:
        if "widget" in kwargs:
            self.widget = kwargs.pop("widget")
            print("Has widget", self.widget)
            assert(isinstance(self.widget, Widget)), "Please only Provide Widgets"

        self.portinfo = kwargs.pop("info") if "info" in kwargs else None
        self.portdescription = kwargs.pop("description") if "description" in kwargs else None
        self.portprimary = kwargs.pop("primary") if "primary" in kwargs else False
        help_text = kwargs.pop("help_text") if "help_text" in kwargs else self.portdescription

        super(PortMixin, self).__init__(*args, **kwargs, help_text=help_text)


    def build_port(self, key):
        assert (self.widget is not None and isinstance(self.widget, Widget)), "Problematic Port Setup"
        params = self.widget.serialize(self) if self.widget else {}
        try:
            if issubclass(self.default, fields.empty): # Raises exception if not Class
                default = None
            else:
                default = self.default
        except:
            default = self.default

        return {
        "key": key,
        "name": self.label or self.field_name or key,
        "description": self.portdescription or self.help_text,
        "required": self.required,
        "default": default,
        "type": self.type,
        "primary": self.portprimary,
        "widget": params
        }


class ModelPortMixin(PortMixin):

    def __init__(self, model, *args, **kwargs) -> None:
        self.portidentifer = model.__name__
        super().__init__(model, *args, **kwargs)


    def build_port(self, key):
        standard = super().build_port(key)
        
        return { **standard, "identifier": self.portidentifer}


class ModelField(ModelPortMixin, serializers.ModelField):
    type= "model"
    widget = ModelWidget()

class CharField(PortMixin, serializers.CharField):
    type= "char"
    widget = CharWidget()

class IntField(PortMixin, serializers.IntegerField):
    type= "int"
    widget = IntWidget()

class FloatField(PortMixin, serializers.FloatField):
    type= "float"
    widget = FloatWidget()

class ListField(PortMixin, serializers.ListField):
    type= "list"
    widget = ListWidget()

class BoolField(PortMixin, serializers.BooleanField):
    type= "bool"
    widget = SwitchWidget()

class UUIDField(PortMixin, serializers.BooleanField):
    type= "uuid"
    widget = UUIDWidget()


#TODO: Refactor into seperate module

class Object(serializers.Serializer):
    type = "object"
    widget = ObjectWidget()

class Inputs(serializers.Serializer):
    pass

class Outputs(serializers.Serializer):
    pass

class DummyInputs(serializers.Serializer):
    dummy = CharField(help_text= "This is just a Dummy")

class DummyOutputs(serializers.Serializer):
    dummy = CharField(help_text= "This is just a Dummy")


def FilteredModelField(model, filterkwargs, *args, **kwargs):
    return PrimaryKeyRelatedField(queryset=model.objects.filter(**filterkwargs).all(),*args, **kwargs)