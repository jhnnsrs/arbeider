from delt.models import DataModel, DataPoint
from django.db import models
from django.conf import settings
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

EXTENSION_MODELS = None


def buildModelIdentifier(model):

    return f"{model.__name__}"





def get_extension_models():
    global EXTENSION_MODELS
    if EXTENSION_MODELS == None:
        allmodels = apps.get_models()
        EXTENSION_MODELS = []


        for model in allmodels:
            try: 
                identifiers = model._meta.identifiers
            except:
                continue

            try:

                datapoint = DataPoint.objects.get(name=model._meta.app_label)
                datamodel, created = DataModel.objects.update_or_create(point= datapoint, 
                            identifier=buildModelIdentifier(model),
                            extenders=identifiers,
                )
                if created: logger.info("Registered new datamodel!")
                EXTENSION_MODELS.append(datamodel)

            except DataPoint.DoesNotExist:
                logger.error("You have models that provide extenders but are not part of a registere Datapoint app, please register")
                continue
                


    return EXTENSION_MODELS



class Model(models.Model):
    identifier = None

    class Meta:
        abstract = True