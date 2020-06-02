
import logging


from delt.discover import ROUTER_BACKENDS_FIELD, ROUTER_TYPE
from delt.models import Node, Route
from delt.register import BaseRegister, BaseRegisterConfigurationError
from delt.registry import get_registry
from delt.routers.utils import route_identifier
from konfig.node import Konfig

logger = logging.getLogger(__name__)

class RouterRegistryConfigurationError(BaseRegisterConfigurationError):
    pass

class RouterRegisterSettings(RouterRegistryConfigurationError):
    enforce_catalog = False
    enforce_registry = False
    provider = None
    settingsField = ROUTER_BACKENDS_FIELD


class RouterRegister(BaseRegister):
    type = ROUTER_TYPE
    register: Route = None
    provider = None
    settings = None

    def __init__(self, node: Node, **kwargs):
        if self.register is None or not issubclass(self.register, Route):
            raise RouterRegistryConfigurationError("Please specifiy a subclass for Route ")
        if node is None or not isinstance(node, Node):
            raise RouterRegistryConfigurationError(f"Node must be a subclass of Node: is {node} ")
        self._node = node
        self._routeidentifier = None
        super().__init__(**kwargs)

    def get_route_identifier(self):
        # Will help to identifiy the Node within the Framework
        if self._routeidentifier is None:
            self._routeidentifier = route_identifier(self._node.package, self._node.interface, self.provider)
        # The Indentifier should be unique for each
        return self._routeidentifier