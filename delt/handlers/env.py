from abc import ABC
from delt.selectors.base import BaseSelector
from typing import Generic, TypeVar
from delt.models import Provider, ProviderSettings
import logging
from django.db.utils import ProgrammingError

logger = logging.getLogger(__name__)

Settings = TypeVar("Settings")
Selector = TypeVar("Selector")

class SettingsError(Exception):
    pass

class BaseHandlerEnvironment(ABC, Generic[Settings,Selector]):
    settingsModel: Settings = ProviderSettings
    selectorClass: Selector = BaseSelector

    def __init__(self, settingsField, **kwargs) -> None:
        self.active = True
        self.settings: Settings = None
        # No matter the Database settings this needs to be initialized
        self.gateway_channel = f"{settingsField}_gateway"
        self.channel_channel = f"{settingsField}_channel"
        self.provider_name = settingsField

        settingsSettings = {
            "active" : True
        } # TODO: Get these from the settings object in the django settings, this will be the default settings for every setup.

        assert self.selectorClass is not None, "You need to provide a selectorClass in your BaseHandler"

        overwrittenSettings = {**settingsSettings, **kwargs}
        try:
            provider, created = Provider.objects.get_or_create(name=settingsField)
            if created: logger.warn("Appears we are having an initial setup!")
        except:
            logger.error("Please migrate first!!!")
            return
            
        try:
            try:
                self.settings = self.settingsModel.objects.filter(provider=provider).latest("created_at") 
            except Exception as e:
                logger.warn(f"We found no personalised settings in Django, We are using the default values from Settings! {e}")
                try:
                    self.settings = self.settingsModel.objects.create(provider=provider,**overwrittenSettings)
                except Exception as e:
                    logger.error(f"Settings for {provider} are not sufficient enough. Please specifiy them manually in the Admin Interface and restart! {e}")
        except ProgrammingError as e:
            logger.error("Migrations need to run first!")
            # Let that be overridden by the settings#
            # find handler settings


    def getSelectorFromKwargs(self, kwargs: dict) -> Selector:
        serialized = self.selectorClass(data=kwargs)
        if serialized.is_valid(raise_exception=True):
            return serialized.validated_data

    def getSettings(self) -> Settings:
        return self.settings

    def getGatewayChannelName(self) -> str:
        return self.gateway_channel

    def getChannelChannelName(self) -> str:
        return self.channel_channel

    def getProviderName(self) -> str:
        return self.provider_name

    def getProvider(self) -> Provider:
        return Provider.objects.get(name=self.getProviderName())
            

    
