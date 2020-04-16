from delt.exceptions import DeltConfigError
from django.conf import settings

def get_default_job_settings():
    try:
        if settings.DEFAULT_JOB_SETTINGS is not None: return settings.DEFAULT_JOB_SETTINGS
    except AttributeError as e: 
        return {
                "reload" : True
        }

def get_default_args():
    try:
        if settings.DEFAULT_ARGS_SETTINGS is not None: return settings.DEFAULT_ARGS_SETTINGS
    except AttributeError as e: 
        return {
                "dummy" : { "type": "model" 
                            , "sd": "dummy", "value": None}
        }