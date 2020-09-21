from django.db.models.fields.files import ImageField
import graphene
from django.contrib.postgres.fields.jsonb import JSONField
from graphene_django.converter import convert_django_field

from balder.fields import Inputs, Outputs, Image
from delt.fields import InputsField, OutputsField
from django.db.models import ImageField




@convert_django_field.register(OutputsField)
def convert_json_field_to_string(field, registry=None):
    return Inputs()

@convert_django_field.register(InputsField)
def convert_json_field_to_string(field, registry=None):
    return Outputs()

@convert_django_field.register(ImageField)
def convert_field_to_string(field, registry=None):
    return Image(field, description=field.help_text, required=not field.null)

class Registry():

    def __init__(self):
        self.fieldQueryMap = {}
        self.fieldSubscriptionMap = {}
        self.fieldMutationMap = {}
        self.nodeSubscriptionMap = {}

    def getQueryFields(self):
        return self.fieldQueryMap
    
    def setSubscriptionForNode(self, node, value):
        self.nodeSubscriptionMap[node.id] = value

    def getSubscriptionForNode(self, node):
        if node.id in self.nodeSubscriptionMap:
            return self.nodeSubscriptionMap[node.id]
        else:
            raise Exception(f"Did Not find Subscription for Node {node.id}. Fields are {self.nodeSubscriptionMap}")

    def setQueryField(self, field, value):
        self.fieldQueryMap[field] = value

    def getSubscriptionFields(self):
        return self.fieldSubscriptionMap
    
    def setSubscriptionField(self, field, value):
        self.fieldSubscriptionMap[field] = value

    def getMutationFields(self):
        return self.fieldMutationMap
    
    def setMutationField(self, field, value):
        self.fieldMutationMap[field] = value


registry = None

def get_registry()-> Registry:
    global registry
    if registry is None:
        registry = Registry()
    return registry
