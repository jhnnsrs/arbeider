from delt.models import Assignation
from django.db import models
from typing import Type
from rest_framework import serializers


def messenger(model: Type[models.Model]):

    fields = {
        "instance" :serializers.PrimaryKeyRelatedField(queryset=model.objects.all())
    }

    Messenger = type(model.__name__+"Messenger", (serializers.Serializer,),{ **fields, "__doc__": f"This is a Messenger for {model.__name__}"})

    packing = lambda x: Messenger({"instance" : x}).data
    
    def unpacking (payload):
        serializer = Messenger(data=payload)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.validated_data["instance"]
            return instance

    return packing, unpacking






packAssignation, unpackAssignation = messenger(Assignation)