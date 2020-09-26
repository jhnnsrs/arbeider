from delt.constants.lifecycle import POD_ACTIVE
import logging
from delt.pods.base import (PodBackendRegister,
                            PodBackendRegisterConfigurationError,
                            PodBackendSettings)
from delt.registry import get_registry
from delt.utils import props
from kanal.consumers.asynchronous.base import KanalAsyncConsumer
from kanal.consumers.sync.base import KanalSyncConsumer
from kanal.models import KanalPod
from konfig.node import Konfig

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
    register = KanalPod
    _channel = None
    settings = KanalSettings()

    def __init__(self, konfig: Konfig, channel = None, **kwargs):
        """A decorate to facilitate the integration of ChannelConsumers into the Framework
        
        Arguments:
            konfig {Konfig} -- Either provide on or the other
            node {Node} -- Either provide on or the other
            channel {str} -- The channel this Consumers/Node listens. If None a custom channelname will be constructed with the nodeidentifer
            kwargs {str} -- Additional Kwars for Model Creation
        """
        self._channel = channel
        self.self_properties = props(self)
        self.konfig_properties = props(konfig)
        self.konfig = konfig
        # Every konfig that was registered will have a Node attached
        super().__init__(konfig.get_node(), **kwargs)

    def catalog_class(self, cls,**kwargs):
        """Implement your Custom Cataloginc Logic Here
        Hint: 
            You should consider using the get_additional_uniques and get_additional_kwargs and setting
            Register, 
        Arguments:
            cls {class} -- The Class that is to be catalgoed
        """
        logger.debug(f"Adding {cls.__name__} to Pods")
        node = self._node
        # The Register as a Subclass of Node

        register: Pod =  self.get_value_in_derived("register")
        # Will help to identifiy the Node within the Framework

        persistent = self.get_value_in_derived("persistent")
        provider = self.get_value_in_derived("provider")
        podclass = self.get_value_in_derived("podclass", default=self.get_default_podclass())


        nodeDefaults = {
            "node" : node,
            "persistent":  persistent,
            "podclass" : podclass,
            "provider" : provider,
            "status": POD_ACTIVE
        }

        nodeUniques = {

        }

        additionalKwargs = self.get_additional_kwargs()
        additionalUniques = self.get_additional_uniques()

        nodeDefaults.update(additionalKwargs)
        nodeUniques.update(additionalUniques)

        if not bool(nodeUniques):
            raise PodBackendRegisterConfigurationError("Please provided at least one unique identifier if you register through this backend")
        # Register With Backend if channel and node
        if issubclass(self.konfig, Konfig): # A Check
            logger.debug(f"Registering {cls.__name__} wtih {register.__name__}")
            try:
                pod = register.objects.get(**nodeUniques)
                for key, value in nodeDefaults.items():
                    setattr(pod, key, value)
                pod.save()
                logger.debug(f"Updated Pod on Node {node.name}")
            except KanalPod.DoesNotExist:
                combined = {**nodeUniques}
                combined.update(nodeDefaults)
                pod = register(**combined)
                pod.save()
                logger.info(f"Created Pod on Node {node.name}")
            logger.debug("Registered succesfully")
        
        else:
            raise NotImplementedError(f"Not Sure how to register {cls.__name__}")

        return pod

    def get_value_in_derived(self, key, default=None):
        """Searches in ascdening order for overwritten properties 

        Register -> Config -> default

        None elements are ignored and resort to KeyError
        
        Arguments:
            key {str} -- The Property
        
        Keyword Arguments:
            default {bool} -- The default it should resort to if no property is detected (default: {None})
        
        Raises:
            KeyError: If the Property doesnt exist and no default was set
        
        Returns:
            any -- Returns the property
        """
        if key in self.self_properties and self.self_properties[key] is not None:
            return self.self_properties[key]
        elif key in self.konfig_properties and self.konfig_properties[key] is not None:
            return self.konfig_properties[key]
        else:
            if default is not None: return default
            raise KeyError(f" '{key}' does not exist in {self.konfig.__name__} or {self.__class__.__name__}")

    def get_default_podclass(self):
        return "kanal-pod"

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
        if not issubclass(cls, KanalSyncConsumer) and not issubclass(cls, KanalAsyncConsumer):
            raise IsNotConsumer(f"{cls.__name__} does not inherit from BaseConsumer. Cannot Register!")
            #TODO: Find inheritance for all Consumers

        cls.konfig = self.konfig
        cls.channel = self.get_channel()
        return cls

    def register_class(self, cls):
        get_registry().registerChannelConsumer(self.get_channel(), cls)

    def cls_to_be_returned(self, cls):
        logger.debug(f"Setting Channel and Config Property on Class {cls.__name__}")
        channel = self.get_channel()
        cls.konfig = self.konfig
        cls.channel = channel
        return cls


class register_with_kanal_backend(KanalRegistry):
    pass