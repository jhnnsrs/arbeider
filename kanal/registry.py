import logging

from delt.pods.base import PodBackendRegister, PodBackendSettings, PodBackendRegisterConfigurationError
from delt.registry import get_registry
from kanal.models import KanalPod
logger = logging.getLogger(__name__)
#CHANNELS_JOB_ACTION = "emit_job"

class IsNotConsumer(PodBackendRegisterConfigurationError):
    pass

class KanalSettings(PodBackendSettings):
    enforce_catalog = False
    enforce_register = False
    provider = "kanal"


class KanalRegistry(PodBackendRegister):
    persistent = True
    provider = "kanal"
    _channel = None
    settingsClass = KanalSettings

    def __init__(self, config, channel = None, **kwargs):
        """A decorate to facilitate the integration of ChannelConsumers into the Framework
        
        Arguments:
            channel {str} -- The channel this Consumers/Node listens. If None a custom channelname will be constructed with the nodeidentifer
            kwargs {str} -- Additional Kwars for Model Creation
        """
        self._channel = channel
        super().__init__(config, **kwargs)

    def get_default_podclass(self):
        return "classic-node"

    def get_additional_uniques(self):
        return {
            "channel": self.get_channel()
        }

    def get_channel(self):
        if self._channel is None:
            self._channel = "channel_"+ self.get_pod_identifier()
            return self._channel
        else:
            return self._channel

    def cls_to_be_registered(self,cls):
        if issubclass(cls, object) is False:
            raise IsNotConsumer(f"{cls.__name__} does not inherit from BaseConsumer. Cannot Register!")
            #TODO: Find inheritance for all Consumers

        cls.config = self.config
        cls.channel = self.get_channel()
        return cls

    def register_class(self, cls):
        get_registry().registerChannelConsumer(self.get_channel(), cls)

    def cls_to_be_returned(self, cls):
        logger.info(f"Setting Channel and Config Property on Class {cls.__name__}")
        channel = self.get_channel()
        cls.config = self.config
        cls.channel = channel
        return cls


class register_with_kanal_backend(KanalRegistry):
    register = KanalPod