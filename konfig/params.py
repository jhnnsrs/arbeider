from typing import List
import graphene
from konfig.widgets import Widget, CharWidget, FileWidget, FloatWidget, IntWidget, ListWidget, ModelWidget, ObjectWidget, SwitchWidget, UUIDWidget, Widget
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

    @classmethod
    def types(cls):
        return { 
            "type": str, 
            "key": str,
            "label": str,
            "dependencies": List[str],
            "description": str,
            "required": bool,
            "primary": bool,
            "widget": Widget,
        **cls.paramTypes()}

    def params(self, key, depth=0):
        return {}

    @classmethod
    def paramTypes(cls):
        return {}

    def build_port(self, key, depth=0):
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
        "label": self.label or self.field_name or key,
        "description": self.portdescription or self.help_text,
        "required": self.required,
        "default": default,
        "type": self.type,
        "primary": self.portprimary,
        "widget": params,
        **self.params(key, depth=depth)
        }


class ModelPortMixin(PortMixin):

    def __init__(self, model, *args, querybuilder= lambda x: x.objects.all(), **kwargs) -> None:
        self.portidentifer = model.__name__
        super().__init__(*args, queryset= querybuilder(model),**kwargs)


    
    def params(self, key, depth=0):
        return {
            "identifier": self.portidentifer
        }

    @classmethod
    def paramTypes(cls):
        return {
            "identifier": str
        }



class ObjectPortMixin(PortMixin):
    widget= ObjectWidget()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)


    def params(self, key, depth=0):

        if (depth >= 3): raise NotImplementedError("Maximum recursion of Objects exceeded")
        argsfields = self.fields #We are dealing with an Instance
        subports = []
        for subkey, subfield in argsfields.items():
            assert(isinstance(subfield, PortMixin)), "Fiedls of ObjectPort must be implementing PortMixin"
            subports.append(subfield.build_port(f"{key}.{subkey}", depth=depth+1))
        return {
            "ports": subports
        }

    
    @classmethod
    def paramTypes(cls):
        return {
            "ports": List[PortMixin]
        }
       


class ModelPort(ModelPortMixin, PrimaryKeyRelatedField):
    type= "model"
    widget = ModelWidget()
    description="This is a Model Port"

class CharPort(PortMixin, serializers.CharField):
    type= "char"
    widget = CharWidget()
    description="This is a Model Port"


class FilePort(PortMixin, serializers.FileField):
    type= "file"
    widget = FileWidget()
    description="This is a Model Port"

class IntPort(PortMixin, serializers.IntegerField):
    type= "int"
    widget = IntWidget()
    description="This is a Model Port"

    @classmethod
    def paramTypes(cls):
        return {
            "default": int
        }

class FloatPort(PortMixin, serializers.FloatField):
    type= "float"
    widget = FloatWidget()
    description="This is a Model Port"

    @classmethod
    def paramTypes(cls):
        return {
            "default": float
        }

class ListPort(PortMixin, serializers.ListField):
    type= "list"
    widget = ListWidget()
    description="This is a Model Port"

    @classmethod
    def paramTypes(cls):
        return {
            "default": List
        }

class BoolPort(PortMixin, serializers.BooleanField):
    type= "bool"
    widget = SwitchWidget()
    description="This is a Model Port"

class UUIDPort(PortMixin, serializers.BooleanField):
    type= "uuid"
    widget = UUIDWidget()
    description="This is a Model Port"


#TODO: Refactor into seperate module

class ObjectPort(ObjectPortMixin, serializers.Serializer):
    type = "object"
    widget = ObjectWidget()
    description="This is a Model Port"






class Inputs(serializers.Serializer):
    pass

class Outputs(serializers.Serializer):
    pass

class DummyInputs(serializers.Serializer):
    dummy = CharPort(help_text= "This is just a Dummy")

class DummyOutputs(serializers.Serializer):
    dummy = CharPort(help_text= "This is just a Dummy")


def FilteredModelField(model, filterkwargs, *args, **kwargs):
    return PrimaryKeyRelatedField(queryset=model.objects.filter(**filterkwargs).all(),*args, **kwargs)