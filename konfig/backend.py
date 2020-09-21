import logging

from django.utils.html import escape
from delt.node import node_identifier
from delt.nodes.base import (NodeBackendRegister,
                             NodeBackendRegisterConfigurationError,
                             NodeBackendSettings)
from delt.orchestrator import get_orchestrator
from delt.utils import compareNodes, props
from konfig.models import KonfigNode
from konfig.node import Konfig
from konfig.utils import parse_inputs, parse_outputs
from konfig.validator import KonfigValidator

logger = logging.getLogger(__name__)

class IsNotKonfig(NodeBackendRegisterConfigurationError):
    pass

class KonfigSettings(NodeBackendSettings):
    enforce_catalog = False
    enforce_register = False
    provider = "konfig"


class KonfigBackend(NodeBackendRegister):
    register = KonfigNode
    provider = "konfig"
    _channel = None
    settings = KonfigSettings()

    def __init__(self, konfig: Konfig, **kwargs):
        """A decorate to facilitate the integration of ChannelConsumers into the Framework
        
        Arguments:
            channel {str} -- The channel this Consumers/Node listens. If None a custom channelname will be constructed with the nodeidentifer
            kwargs {str} -- Additional Kwars for Model Creation
        """

        # First we introspect the class and config
        self.self_properties = props(self)
        self.konfig_properties = props(konfig)
        self.konfig = konfig
        super().__init__( **kwargs)

    def get_default_nodetype(self):
        raise NotImplementedError("Please specifiy a default Nodetype to Return")

    def get_node_identifier(self):
        # Will help to identifiy the Node within the Framework
        if self._nodeidentifier is None:
            package = self.get_value_in_derived("package")
            interface = self.get_value_in_derived("interface")
            self._nodeidentifier = node_identifier(package, interface)
            # The Indentifier should be unique for each
        return self._nodeidentifier


    def catalog_class(self, cls,**kwargs):
        """Implement your Custom Cataloginc Logic Here
        Hint: 
            You should consider using the get_additional_uniques and get_additional_kwargs and setting
            Register, 
        Arguments:
            cls {class} -- The Class that is to be catalgoed
        """
        logger.debug(f"Evaluating {cls.__name__}")

        # The Register as a Subclass of Node
        register  =  self.register

        # Will help to identifiy the Node within the Framework
        realm = self.get_value_in_derived("provider")
        package = self.get_value_in_derived("package")
        interface = self.get_value_in_derived("interface")

        # The Indentifier should be unique for each
        identifier = self.get_node_identifier()

        # General
        name = self.get_value_in_derived("name", default=cls.__name__)
        description = escape(self.get_value_in_derived("description", default=self.konfig.__doc__ or "No Description"))

        # Graph Related
        inputs = parse_inputs(self.konfig)
        outputs = parse_outputs(self.konfig)
        nodeclass = self.get_value_in_derived("nodeclass", default=self.get_default_nodetype())
        variety = self.get_value_in_derived("variety")

        # Publishers
        publishers = self.get_value_in_derived("publishers", default=self.settings.defaultPublishers)


        nodeDefaults = {
            "realm": realm,
            "package" : package,
            "interface" : interface,
            "publishers" : publishers,
            "name":  name,
            "description" : description,
            "inputs" : inputs,
            "outputs" : outputs,
            "nodeclass" : nodeclass,
            "variety" : variety,
        }

        nodeUniques = {
            "identifier" : identifier,

        }

        additionalKwargs = self.get_additional_kwargs()
        additionalUniques = self.get_additional_uniques()

        nodeDefaults.update(additionalKwargs)
        nodeUniques.update(additionalUniques)


        # Register With Backend if channel and node
        if issubclass(self.konfig, Konfig): # A Check
            logger.debug(f"Registering {cls.__name__} wtih {register.__name__}")
            try:
                node = register.objects.get(**nodeUniques)
                updated = compareNodes(node, nodeDefaults)
                if bool(updated):
                    for key, value in updated.items():
                        if key == "outputs" or key == "inputs":
                            logger.info(f"Updated {key} on {package}/{interface}")
                        else: 
                            logger.info(f"Updated {key} to {value} on {package}/{interface}")
                
                for key, value in nodeDefaults.items():
                    setattr(node, key, value)
                node.save()
                logger.debug(f"Updated {package}/{interface} on Identifier: {identifier}")
            except KonfigNode.DoesNotExist:
                combined = {**nodeUniques}
                combined.update(nodeDefaults)
                node = register(**combined)
                node.save()
                logger.info(f"Created {package}/{interface} on Identifier: {identifier}")
            logger.debug("Registered succesfully")
        
        else:
            raise NotImplementedError(f"Not Sure how to register {cls.__name__}")

        return node


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

    def get_default_nodetype(self):
        return "konfig-node"

    def cls_to_be_registered(self,cls): 
        return cls

    def register_class(self, cls):
        pass

    def cls_to_be_returned(self, cls):
        logger.info(f"Registering {cls}")
        get_orchestrator().setValidatorForNodeIdentifier(self.get_node_identifier(), KonfigValidator(self.konfig))
        return cls


class register_konfig_node(KonfigBackend):
    pass