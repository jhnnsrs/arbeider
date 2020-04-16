import logging

from delt.nodebackends.base import NodeBackendRegister, NodeBackendSettings, NodeBackendRegisterConfigurationError
from .models import FrontendNode
from delt.registry import get_registry

logger = logging.getLogger(__name__)

class FrontendNodeType():
    pass

class IsNotFrontEnd(NodeBackendRegisterConfigurationError):
    pass

class FrontendSettings(NodeBackendSettings):
    enforce_update = False
    provider = "frontend"


class FrontendBackend(NodeBackendRegister):
    provider = "frontend"
    settingsClass = FrontendSettings

    def __init__(self, *args, path = None, **kwargs):
        """A decorate to facilitate the integration of Nodes into the Framework
        
        Arguments:
            path {str} -- The path sits on
            kwargs {str} -- [description]
        """
        super().__init__(*args,**kwargs)
        self._path = path

    def get_additional_kwargs(self):
        path =  self.get_value_in_derived("path")
        return {
            "path": path
        }

    def get_default_nodetype(self):
        return "classic-node"

    def get_path(self):
        if self._path is None:
            self._path = self.get_value_in_derived("path")
            return self._path
        else:
            return self._path

    def cls_to_be_registered(self,cls):
        if issubclass(cls, FrontendNodeType) is False:
             raise IsNotFrontEnd(f"{cls.__name__} does not inherit from FrontendNodeType. Cannot Register!") 
        return cls

    def cls_to_be_returned(self, cls):
        return cls



class register_with_fremmed_backend(FrontendBackend):
     register = FrontendNode