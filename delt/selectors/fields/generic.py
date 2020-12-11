from delt.selectors.fields.base import FieldMixin


from delt.widgets.widgets.generic import IntWidget, BoolWidget
from rest_framework import serializers

class IntField(FieldMixin, serializers.IntegerField):
    type= "int"
    widget = IntWidget()
    description="This is a Model Port"


class BoolField(FieldMixin, serializers.BooleanField):
    type = "bool"
    widget = BoolWidget()
    description = "A simple boolean widget"
