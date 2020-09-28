""" The Discover Module """

import logging
import os
from importlib import import_module

from django.conf import settings
from delt.registry import get_registry

logger = logging.getLogger(__name__)

DEFAULT_DISCOVER_PATH = "nodes"

ROUTER_BACKENDS_FIELD = "ROUTER_BACKENDS"
ROUTER_TYPE = "routers"

NODE_BACKENDS_FIELD = "NODE_BACKENDS"
NODE_BACKEND_TYPE  = "nodes"

PUBLISHER_BACKENDS_FIELD = "PUBLISHERS"
PUBLISHER_BACKEND_TYPE  = "publishers"

POD_BACKENDS_FIELD = "POD_BACKENDS"
POD_BACKEND_TYPE  = "pods"

class DiscoverMember:
    field = None
    type = None

class NodeBackendMember(DiscoverMember):
    field = NODE_BACKENDS_FIELD
    type = NODE_BACKEND_TYPE

class PodMember(DiscoverMember):
    field = POD_BACKENDS_FIELD
    type = POD_BACKEND_TYPE

class RouterMember(DiscoverMember):
    field = ROUTER_BACKENDS_FIELD
    type = ROUTER_TYPE

class PublisherMember(DiscoverMember):
    field = PUBLISHER_BACKENDS_FIELD
    type = PUBLISHER_BACKEND_TYPE


class NotDiscoveringError(Exception):
    pass

def getDiscover():
    return os.getenv("DELT_DISCOVERING") == "True"

def setDiscover(active):
    it = "True" if active else "False"
    logger.debug(f"DISCOVERING")
    os.environ["DELT_DISCOVERING"] = it


def getCatalog(backend, type):
    return os.getenv("DELT_ENSURE_CATALOG_" + type.upper() + "_" + backend.upper(), "False") == "True"

def getRegister(backend, type):
    return os.getenv("DELT_ENSURE_REGISTER_" + type.upper() + "_" + backend.upper(), "False") == "True"

def setCatalog(active, backend, type):
    active_string = "True" if active else "False"
    logger.debug(f"SETTING {type} CATALOG TO {active_string} for {backend}")
    os.environ["DELT_ENSURE_CATALOG_" + type.upper() + "_" + backend.upper()] = active_string

def setRegister(active, backend, type):
    active_string = "True" if active else "False"
    logger.debug(f"Setting {type} Register to {active_string}")
    os.environ["DELT_ENSURE_REGISTER_" + type.upper() + "_" + backend.upper()] = active_string

def discover_path(thepath, backend, base, catalog=False, register=False, type= type):
    
    # Set Environment so that the Backends know if to register or not
    if catalog:
       setCatalog(True, backend, type)
    if register:
       setRegister(True, backend, type)

    for app in settings.INSTALLED_APPS:
        # For each app, we need to look for an consumers.py inside that app's
        # package. We can't use os.path here -- recall that modules may be
        # imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for admin.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own admin registration.
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue
        # Step 2: import the app's nodes file. If this has errors we want them
        # to bubble up.
        try:
            logger.info(f"Importing {thepath}")
            if base is not None:
                modulepath = f"{app}.{base}.{thepath}"
            else:
                modulepath = f"{app}.{thepath}"
            import_module(modulepath, package=True)
            logger.info(f"Imported {backend} at {app}")
        except ImportError as e:
            if app in settings.MODULES:
                if f"No module named '{app}" in str(e):
                    logger.info(f"No Modules for {backend} found for {app} at {modulepath} {e}")
                else:
                    logger.error(f"Unable to import {backend} found for {app} at {modulepath} {e}")
                    raise e
            continue

    # Unset Environment so that the Backends know if to register or not
    if catalog:
       setCatalog(False, backend, type)
    if register:
       setRegister(False, backend, type)


def discover_from_config(config: dict, provider: str, type = None , catalog = False, register = False):
    if "autodiscover" in config and config["autodiscover"] is True:
        logger.debug(f"Discovering modules for {provider}")
        base = config["base"] if "base" in config else None
        if "path" in config and config["path"] is not None:
            discover_path(config["path"], provider, base, catalog=catalog, register=register, type= type)
    else:
        logger.warn(f"{provider} has disabled Autodisovery")



def autodiscover(member: DiscoverMember, backend = None, catalog = False, register=False):

    setDiscover(True)

    if not hasattr(settings, member.field):
        raise NotImplementedError(f"We didnt find a configuration to autodiscover from. Please implement {member.field} in your settings.")

    backends = getattr(settings, member.field)
    if backend is not None:
        logger.info(f"Trying to import {member.type}-Pods in all Apps")
        try:
            config = backends[backend]
        except KeyError:
            raise NotImplementedError(f"No {member.field} configuration found for {backend}")
        discover_from_config(config, backend, type=member.type , catalog=catalog, register = register,)
          
    else: 
        logger.info(f"Trying to import all {member.type} in all Apps")
        for backend, config in backends.items():
            discover_from_config(config, backend, type=member.type  , catalog=catalog, register = register,)

    setDiscover(False)
    # The Registry we return holds all information of the registered Nodes according to their backend
    return get_registry()




def autodiscover_pods(*args, **kwargs):
    """ This function will be importing all Pods in the app directorys, if
     DELT_ENSURE_REGISTER env is set to True it will also try to register all nodes
     with the database"""
    return autodiscover(PodMember, *args, **kwargs)

def autodiscover_nodes(*args, **kwargs):
    """ This function will be importing all Nodes in the app directorys, if
     DELT_ENSURE_REGISTER env is set to True it will also try to register all nodes
     with the database"""
    return autodiscover(NodeBackendMember, *args, **kwargs)

def autodiscover_routers(*args, **kwargs):
    """ This function will be importing all Nodes in the app directorys, if
     DELT_ENSURE_REGISTER env is set to True it will also try to register all nodes
     with the database"""
    return autodiscover(RouterMember, *args, **kwargs)


def autodiscover_publishers(*args, **kwargs):
    """ This function will be importing all Nodes in the app directorys, if
     DELT_ENSURE_REGISTER env is set to True it will also try to register all nodes
     with the database"""
    return autodiscover(PublisherMember, *args, **kwargs)
