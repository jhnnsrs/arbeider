import logging

from django.conf import settings

from delt.models import Assignation, Node, Pod, Provision

logger = logging.getLogger(__name__)



class BaseHandlerException(Exception):
    pass

class BaseHandlerConfigException(Exception):
    pass

class BaseHandlerSettings(object):
    provider = None
    settingsField = "HANDLERS"

    def __init__(self, *args, **kwargs):
        if self.provider is None:
            raise NotImplementedError("Please Provide a provider in your HandlerSettings")
        #Set Defaults from config
        if hasattr(settings, self.settingsField):
            providers = getattr(settings,self.settingsField)
            if self.provider in providers:
                for key, value in providers[self.provider].items():
                    logger.debug(f"Overwriting {key} with {value} at {self.provider} in {self.settingsField}")
                    setattr(self,key,value)


class BaseHandler(object):
    provider = None
    settings = None

    def __init__(self, *args, **kwargs):
        if self.provider is None: raise BaseHandlerConfigException("Please register your Handler with a Provider")
        if self.settings is None or not isinstance(self.settings, BaseHandlerSettings):
            raise BaseHandlerConfigException("Please Provide a settingsClass in your Handler")
        super().__init__()

    def on_assign_job(self, assignation: Assignation):
        raise NotImplementedError

    def on_provide_pod(self, reference: str, node: Node, substring: str, user):
        raise NotImplementedError

    def on_new_provision(self, provision: Provision):
        raise NotImplementedError

    def on(self, field):
        try:
            method = getattr(self, f"on_{field}")
            assert callable(method)
            return method
        except AttributeError:
            logger.error(f"This Handler doesnt know how to handle this event, please provide 'on_{field}' in {self.__class__.__name__}")
            return lambda *arg, **kwargs: True
