import logging
from django.conf import settings

logger = logging.getLogger(__name__)



class BaseValidatorSettings(object):
    provider = None
    settingsField = "VALIDATORS"

    def __init__(self, **kwargs):
        if self.settingsField is None or self.provider is None:
            raise NotImplementedError("Please Provide provider and settingsField in your BouncerSettings")
        #Set Defaults from config
        if hasattr(settings, self.settingsField):
            providers = getattr(settings,self.settingsField)
            if self.provider in providers:
                for key, value in providers[self.provider].items():
                    logger.debug(f"Overwriting {key} with {value} at {self.provider} in {self.settingsField}")
                    setattr(self,key,value)



class BaseValidator(object):
    settings = None

    def __init__(self):
        if self.settings is None or not isinstance(self.settings, BaseValidatorSettings):
            raise NotImplementedError("Please Provide provider and settingsField in your Validator Settings")
        super().__init__()


    def validateInputs(self, inputs) -> dict:
        raise NotImplementedError

    def validateOutputs(self, outputs) -> dict:
        raise NotImplementedError


