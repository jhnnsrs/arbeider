from django.db import models

from django.apps import apps
import logging

logger = logging.getLogger(__name__)

EXTENSION_MODELS = None


def get_extension_models():
    global EXTENSION_MODELS
    if EXTENSION_MODELS == None:
        allmodels = apps.get_models()
        EXTENSION_MODELS = {}

        for model in allmodels:
            print("Updating Transcript")
            try: 
                identifiers = model._meta.identifiers
                for identifier in identifiers:
                    if identifier in EXTENSION_MODELS:
                        EXTENSION_MODELS[identifier].append(model.__name__)
                    else:
                        EXTENSION_MODELS[identifier] = [model.__name__]
            except:
                logger.info(f"{model.__name__} is not a valid DeltModel. Please specify identifiers in Meta Class ")


    return EXTENSION_MODELS



class Model(models.Model):
    identifier = None

    class Meta:
        abstract = True