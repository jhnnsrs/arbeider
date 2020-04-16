from delt.routers.base import RouterRegisterSettings, RouterRegister
from delt.registry import get_registry, RegistryError
from .models import JobRoute
from rest_framework import viewsets
import logging

logger = logging.getLogger(__name__)
class IsNotRestViewSet(Exception):
    pass


class JobbRegistrySettings(RouterRegisterSettings):
    enforce_catalog = False
    enforce_register = False
    provider = "jobb"


class JobbRegister(RouterRegister):
    register = JobRoute
    provider = "jobb"
    settingsClass = JobbRegistrySettings

    def __init__(self, config, basename = None, **kwargs):
        """A decorate to facilitate the integration of Nodes into the Framework
        
        Arguments:
            basename {str} -- The basename this viewsets sits on
            kwargs {str} -- [description]
        """
        self._basename = basename
        self._node = None
        super().__init__(config, **kwargs)

    def get_additional_kwargs(self):
        return {}

    def get_basename(self):
        if self._basename is None:
            self._basename = self.get_value_in_derived("interface")
            return self._basename
        else:
            return self._basename

    def register_class(self, cls):
        try: 
            get_registry().registerViewsetRoute(self.get_basename(), { "viewset": cls, "route": self.get_basename()})
        except RegistryError as e:
            logger.warn(f"Couldnt register {cls.__name__}")
       

    def cls_to_be_registered(self, cls):
        if issubclass(cls, viewsets.GenericViewSet) is False:
             raise IsNotRestViewSet(f"{cls.__name__} does not inherit from GenericViewSet. Cannot Register with backend job!") 
        return cls

    def class_cataloged(self, route: JobRoute ):
        self._node = route.node
        print(self._node)
        pass

    def cls_to_be_returned(self, cls):
        logger.info(f"Setting Config and Doc Property on Class {cls.__name__}")
        cls.config = self.config
        cls.node = self._node
        cls.__doc__ = self.config.__doc__
        return cls



class register_with_job_routes(JobbRegister):
    pass