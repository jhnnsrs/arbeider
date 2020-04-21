import logging

from .base import NodeBackendSettings, NodeBackendRegister, NodeBackendRegisterConfigurationError
from delt.registry import get_registry
from delt.models import Node
logger = logging.getLogger(__name__)
#CHANNELS_JOB_ACTION = "emit_job"

class ConfigNode(object):
    pass


class IsNotConfig(NodeBackendRegisterConfigurationError):
    pass

class ConfigNodeSettings(NodeBackendSettings):
    enforce_catalog = False
    enforce_register = False
    provider = "default"


class ConfigRegistry(NodeBackendRegister):
    register = Node
    provider = "default"
    _channel = None
    settingsClass = ConfigNodeSettings

    def __init__(self, config, **overwrites):
        """A decorate to facilitate the integration of ChannelConsumers into the Framework
        
        Arguments:
            channel {str} -- The channel this Consumers/Node listens. If None a custom channelname will be constructed with the nodeidentifer
            kwargs {str} -- Additional Kwars for Model Creation
        """
        self._overwrites = overwrites or {}
        super().__init__(config)

    def get_default_nodetype(self):
        return "default-node"

    def get_additional_kwargs(self):
        return self._overwrites

    def cls_to_be_registered(self,cls):
        if issubclass(cls, ConfigNode) is False:
            raise IsNotConfig(f"{cls.__name__} does not inherit from NodeConfig. Cannot Register!")
            #TODO: Find inheritance for all Consumers

        return cls

    def register_class(self, cls):
        pass

    def cls_to_be_returned(self, cls):
        return cls


class register_node(ConfigRegistry):
    pass