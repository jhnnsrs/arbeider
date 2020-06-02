import logging

from rest_framework import viewsets

from delt.registry import RegistryError, get_registry
from delt.routers.base import RouterRegister, RouterRegisterSettings
from delt.utils import props
from konfig.node import Konfig

from .models import JobRoute

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
    settings = JobbRegistrySettings()

    def __init__(self, konfig: Konfig, basename = None, **kwargs):
        """A decorate to facilitate the integration of Nodes into the Framework
        
        Arguments:
            basename {str} -- The basename this viewsets sits on
            kwargs {str} -- [description]
        """
        self.konfig = konfig
        self._basename = basename
        self.self_properties = props(self)
        self.konfig_properties = props(konfig)
        super().__init__(konfig.get_node(), **kwargs)

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
        pass

    def cls_to_be_returned(self, cls):
        logger.debug(f"Setting Config and Doc Property on Class {cls.__name__}")
        cls.config = self.config
        cls.node = self._node
        cls.__doc__ = self.config.__doc__
        return cls

    def catalog_class(self, cls, **kwargs):
        """Implement your Custom Cataloginc Logic Here
        Hint: 
            You should consider using the get_additional_uniques and get_additional_kwargs and setting
            Register, 
        Arguments:
            cls {class} -- The Class that is to be catalgoed
        """
        logger.debug(f"Evaluating {cls.__name__}")

        # The Register as a Subclass of Node
        register: Route =  self.register

        # Will help to identifiy the Node within the Framework
        package = self.get_value_in_derived("package")
        interface = self.get_value_in_derived("interface")
        provider = self.get_value_in_derived("provider")

        # The Indentifier should be unique for each
        identifier = self.get_route_identifier()

        # General
        name = self.get_value_in_derived("name", default=cls.__name__)
        description = self.get_value_in_derived("description", default=cls.__doc__ or "No Description")

        # Graph Related

        routeDefaults = {
            "package" : package,
            "interface" : interface,
            "name":  name,
            "description" : description,
            "provider": provider,
            "node": self._node
        }

        # Node
        # If this route is associated with any Route

        routeUniques = {
            "identifier" : identifier,

        }

        additionalKwargs = self.get_additional_kwargs()
        additionalUniques = self.get_additional_uniques()

        routeDefaults.update(additionalKwargs)
        routeUniques.update(additionalUniques)


        # Register With Backend if channel and node
        if issubclass(self.konfig, Konfig): # A Check
            logger.debug(f"Registering {cls.__name__} wtih {register.__name__}")
            try:
                route = register.objects.get(**routeUniques)
                for key, value in routeDefaults.items():
                    setattr(route, key, value)
                route.save()
                logger.debug(f"Updated {package}/{interface} on Identifier: {identifier}")
            except JobRoute.DoesNotExist:
                combined = {**routeUniques}
                combined.update(routeDefaults)
                route = register(**combined)
                route.save()
                logger.info(f"Created {package}/{interface} on Identifier: {identifier}")
            logger.debug("Registered succesfully")
        
        else:
            raise NotImplementedError(f"Not Sure how to register {cls.__name__}")

        return route




class register_with_job_routes(JobbRegister):
    pass