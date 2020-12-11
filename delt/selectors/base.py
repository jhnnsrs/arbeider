from delt.selectors.fields.generic import IntField
from rest_framework import serializers

class BaseSelector(serializers.Serializer):
    __all__ = IntField(required=False)
    pass