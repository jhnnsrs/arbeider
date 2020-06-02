import logging
import re

import graphene
from graphene_django.registry import get_global_registry
from rest_framework import serializers

from balder.builders.utils import generateGrapheneField
from balder.delt_types import JobType, PodType
from balder.subscriptions.job import BaseJobSubscription
from delt.node import NodeConfig
from delt.nodes.base import INPUT_IDENTIFIER, OUTPUT_IDENTIFIER
from elements.types import RepresentationType

logger = logging.getLogger(__name__)

def parse_args(config: NodeConfig):
    ports = {}
    if hasattr(config, INPUT_IDENTIFIER):
        inputs = getattr(config, INPUT_IDENTIFIER)
        argsfields = inputs._declared_fields #We are dealing with an Instance (fields is not accessible)
        for key, field in argsfields.items():
            port = generateGrapheneField(key,field, args= True, prefix="Arguments")
            ports.update(port)
    return ports

def parse_inputs(config: NodeConfig):
    ports = {}
    if hasattr(config, INPUT_IDENTIFIER):
        inputs = getattr(config, INPUT_IDENTIFIER)
        argsfields = inputs._declared_fields #We are dealing with an Instance (fields is not accessible)
        for key, field in argsfields.items():
            port = generateGrapheneField(key,field, prefix="")
            ports.update(port)
    return ports

def parse_outputs(config: NodeConfig):
    ports = {}
    if hasattr(config, OUTPUT_IDENTIFIER):
        outputs = getattr(config, OUTPUT_IDENTIFIER)
        argsfields = outputs._declared_fields #We are dealing with an Instance (fields is not accessible)
        for key, field in argsfields.items():
            port = generateGrapheneField(key,field, prefix="")
            ports.update(port)
    return ports



def generateArguments(config, name):

    genericArguments = {
         "reference" : graphene.String(required=False, description="You should provide this to have an own reference and to avoid resending jobs on connection drop!"),
         "pod" : graphene.ID(required=True),
         "__doc__": config.inputs.__doc__ or "This is the Arguments"
    }
    args = parse_args(config)
    if bool(args):
        return type(name+"Arguments", (object,),{ **genericArguments, **args, "__doc__": "This is the Arguments"})
    else:
        return type(name+"Arguments", (object,),{ **genericArguments, })


def generateOutputFields(config, name):
    outputs = parse_outputs(config)
    if bool(outputs):
        return type(name+"Outputs", (graphene.ObjectType,), { **outputs, "__doc__": "This is the Outputs"})
    else:
        return None

def generateInputFields(config, name):
    inputs = parse_inputs(config)
    if bool(inputs):
        return type(name+"Inputs", (graphene.ObjectType,), { **inputs, "__doc__": "This is the Inputs"})
    else:
        return None


def genericJobSubscriptionBuilder(wrapper, config: NodeConfig, path, *args, **kwargs): 

    name = re.sub(r"[^A-Za-z]+", '', path.capitalize())

    subscriptionFields = {**JobType._meta.fields}

    #Arguments will have the same instances as the Serializer, so you call them with the real Arguments
    arguments = generateArguments(config, name)
    if arguments is not None:
        subscriptionFields["Arguments"] = arguments

    outputs = generateOutputFields(config, name)
    if outputs is not None:
        subscriptionFields["outputs"] =  graphene.Field(outputs, required=False, description="The outputs of this Job")

    #Inputs will then be reversed throught the serializer and passed as the correct isntances
    inputs = generateInputFields(config, name)
    if inputs is not None:
        subscriptionFields["inputs"] =  graphene.Field(inputs, required=False, description="The inputs of this Job")

    return type(name+"Job", (BaseJobSubscription,), {**subscriptionFields, "input_serializer_class" : config.inputs})