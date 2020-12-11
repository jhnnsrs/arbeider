





from typing import List
from delt.widgets.base import BaseWidget
from rest_framework import fields

class FieldMixin(object):
    widget = None
    type = None

    def __init__(self, *args, **kwargs) -> None:
        if "widget" in kwargs:
            self.widget = kwargs.pop("widget")
            assert(isinstance(self.widget, BaseWidget)), "Please only Provide BaseWidgets as Widgets"

        self.portinfo = kwargs.pop("info") if "info" in kwargs else None
        self.portdescription = kwargs.pop("description") if "description" in kwargs else None
        self.portprimary = kwargs.pop("primary") if "primary" in kwargs else False
        help_text = kwargs.pop("help_text") if "help_text" in kwargs else self.portdescription
        super(FieldMixin, self).__init__(*args, **kwargs, help_text=help_text)

    @classmethod
    def types(cls):
        """This function gets called when we are trying to parse this to A Graphene Type

        Returns:
            dict: A Dict of all the Types
        """
        return { 
            "type": str, 
            "key": str,
            "label": str,
            "dependencies": List[str],
            "description": str,
            "required": bool,
            "primary": bool,
            "widget": BaseWidget,
        **cls.paramTypes()}

    def params(self, key, depth=0):
        return {}

    @classmethod
    def paramTypes(cls):
        return {}

    def build_port(self, key, depth=0):
        assert (self.widget is not None and isinstance(self.widget, BaseWidget)), "Problematic Port Setup"
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