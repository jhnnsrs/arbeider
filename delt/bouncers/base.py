import logging
from django.conf import settings 
from delt.bouncers.context import BouncerContext
logger = logging.getLogger(__name__)



class BaseBouncerSettings(object):
    provider = None
    settingsField = "BOUNCERS"

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



class BaseBouncer(object):
    settingsClass = None

    def __init__(self, context: BouncerContext):
        if self.settingsClass is None or not isinstance(self.settingsClass, BaseBouncerSettings):
            raise NotImplementedError("Please Provide an instance of BaseBouncerSettings in your Bouncer class")
        self.context = context
        super().__init__()

    @property
    def user(self):
        return self.context.user

