from django.db.models.fields.files import ImageField
import graphene
from django.contrib.postgres.fields.jsonb import JSONField
from graphene_django.converter import convert_django_field

from balder.fields import Inputs, Outputs, ImageField
from delt.fields import InputsField, OutputsField
from django.db.models import ImageField



class BalderRegistry():

    def __init__(self):
        self.fieldQueryMap = {}
        self.fieldSubscriptionMap = {}
        self.fieldMutationMap = {}
        self.nodeSubscriptionMap = {}
        self.fieldTypes = {}

    def getTypeFields(self):
        return self.fieldTypes

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

    def setTypeField(self, field, value):
        self.fieldTypes[field] = value



registry = None

def get_balder_registry()-> BalderRegistry:
    global registry
    if registry is None:
        registry = BalderRegistry()
    return registry
