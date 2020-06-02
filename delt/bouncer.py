from django.conf import settings
from django.contrib.auth import get_user_model

class BaseBouncerContext(object):

    def __init__(self, request: Request = None, info= None, **kwargs):

        self._authorized = None
        self._scopes = None
        if request is not None:
            self._user = request.user
            self._auth = request.auth
        if info is not None:
            self._user = info.context._scope["user"]
            self._auth = None
            #TODO: Impelement oauth thingy dingy


        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def scopes(self):
        if self._scopes is None:
            if self._auth is not None:
                self._scopes = self._auth.scopes
            else:
                self._scopes = []   
        return self._scopes     

    @property
    def user(self):
        if self._user.id is None:
            self._user = None
        return self._user

        
import logging

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
    settingsClass = BaseBouncerSettings

    def __init__(self):
        if self.settingsClass is None or not issubclass(self.settingsClass, BaseBouncerSettings):
            raise NotImplementedError("Please Provide provider and settingsField in your Register Settings")
        super().__init__()


    def checkContext(context: BaseBouncerContext)-> bool:
        if context.is_authorized