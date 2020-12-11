import logging

from django.conf import settings

from delt.models import Pod

logger = logging.getLogger(__name__)


class BasePublisherError(Exception):
    pass


class BasePublisherConfigError(BasePublisherError):
    pass

class BasePublisherSettings(object):
    settingsField = "PUBLISHERS"
    universal = False
    provider = None
    onall = False
    INCLUDE = None
    EXCLUDE = []
    DEFAULTFIELDS = ["job",
    "pod",
    "model",
    # Provision Specific
    "provision_succeeded",
    "provision_failed",

    # Pod Lifecycle Specific
    "pod_updated",
    "pod_initialized",
    "pod_activated", 
    "republished_provision", 

    # Assignation specific
    "assignation_failed",
    "assignation_succeeded",
    "assignation_progress",
    "assignation_done"]

    def __init__(self, **kwargs):
        if self.settingsField is None or self.provider is None:
            raise NotImplementedError("Please Provide provider and settingsField in your Register Settings")
        #Set Defaults from config
        if hasattr(settings, self.settingsField):
            providers = getattr(settings,self.settingsField)
            if self.provider in providers:
                for key, value in providers[self.provider].items():
                    logger.info(f"Overwriting {key} with {value} at {self.provider} in {self.settingsField}")
                    setattr(self,key,value)

    @property
    def fields(self):
        if self.INCLUDE is None:
            return [item for item in self.DEFAULTFIELDS if item not in self.EXCLUDE]
        else:
            return self.INCLUDE

class BasePublisher(object):
    settingsClass = None

    def __init__(self):
        if self.settingsClass is None:
            raise NotImplementedError("Please provide a settings Class in your Register Settings")
        self._settings = self.settingsClass()
        super().__init__()

    def on(self, field):
        try:
            method = getattr(self, f"on_{field}")
            assert callable(method)
            return method
        except AttributeError:
            if getattr(self, "universal", False):
                logger.error(f"{self.__class__.__name__} doesnt know how to handle this event, please provide 'on_{field}' Method")
            return lambda *arg, **kwargs: True

    @property
    def settings(self):
        if self._settings is None:
            self._settings = self.settingsClass()
        return self._settings
