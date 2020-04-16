""" The Discover Module """

import logging 

from importlib import import_module
import os
from django.conf import settings
from delt.registry import get_registry


logger = logging.getLogger(__name__)

DEFAULT_DISCOVER_PATH = "nodes"

ROUTER_BACKENDS_FIELD = "ROUTER_BACKENDS"
ROUTER_TYPE = "routers"

NODE_BACKENDS_FIELD = "NODE_BACKENDS"
NODEBACKEND_TYPE = "nodebackend"


class NotDiscoveringError(Exception):
    pass

def getDiscover():
    return os.getenv("DELT_DISCOVERING") == "True"

def setDiscover(active):
    it = "True" if active else "False"
    logger.info(f"DISCOVERING")
    os.environ["DELT_DISCOVERING"] = it


def getCatalog(backend, type):
    return os.getenv("DELT_ENSURE_CATALOG_" + type.upper() + "_" + backend.upper(), "False") == "True"

def getRegister(backend, type):
    return os.getenv("DELT_ENSURE_REGISTER_" + type.upper() + "_" + backend.upper(), "False") == "True"

def setCatalog(active, backend, type):
    active_string = "True" if active else "False"
    logger.info(f"SETTING {type} CATALOG TO {active_string} for {backend}")
    os.environ["DELT_ENSURE_CATALOG_" + type.upper() + "_" + backend.upper()] = active_string

def setRegister(active, backend, type):
    active_string = "True" if active else "False"
    logger.info(f"Setting {type} Register to {active_string}")
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
            logger.debug(f"Importing {thepath}")
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


def discover_from_config(config: dict, backend: str, type = None , catalog = False, register = False):
    if "autodiscover" in config and config["autodiscover"] is True:
        logger.info(f"Discovering backends for {backend}")
        base = config["base"] if "base" in config else None
        if "path" in config and config["path"] is not None:
            discover_path(config["path"], backend, base, catalog=catalog, register=register, type= type)
    else:
        logger.warn(f"{backend} has disabled Autodisovery")

def autodiscover_nodes(backend = None, catalog = False, register=False):
    """ This function will be importing all Nodes in the app directorys, if
     DELT_ENSURE_REGISTER env is set to True it will also try to register all nodes
     with the database"""
    
    setDiscover(True)

    if not hasattr(settings, NODE_BACKENDS_FIELD):
        raise NotImplementedError("We didnt find a configuration to autodiscover from. Please implement NODE_BACKENDS in your settings.")

    backends = getattr(settings, NODE_BACKENDS_FIELD)
    if backend is not None:
        logger.info(f"Trying to import {backend} in all Apps")
        try:
            config = backends[backend]
        except KeyError:
            raise NotImplementedError(f"No NODE_BACKEND found for {backend}")
        discover_from_config(config, backend, type=NODEBACKEND_TYPE, catalog=catalog, register = register,)
          
    else: 
        logger.info("Trying to import all Backend in all Apps")
        for backend, config in settings.NODE_BACKENDS.items():
            discover_from_config(config, backend, type=NODEBACKEND_TYPE, catalog=catalog, register = register,)

    setDiscover(False)
    # The Registry we return holds all information of the registered Nodes according to their backend
    return get_registry()



def autodiscover_routes(backend = None, catalog = False, register=False, type="router"):
    """ This function will be importing all Nodes in the app directorys, if
     DELT_ENSURE_REGISTER env is set to True it will also try to register all nodes
     with the database"""
    
    setDiscover(True)

    if not hasattr(settings, ROUTER_BACKENDS_FIELD):
        raise NotImplementedError("We didnt find a configuration to autodiscover from. Please implement ROUTES_BACKENDS in your settings.")

    backends = getattr(settings, ROUTER_BACKENDS_FIELD)
    if backend is not None:
        logger.info(f"Trying to import Routes from {backend} in all Apps")
        try:
            config = backends[backend]
        except KeyError:
            raise NotImplementedError(f"No ROUTERS_BACKEND found for {backend}")
        discover_from_config(config, backend, type=ROUTER_TYPE, catalog=catalog, register = register)
          
    else: 
        logger.info("Trying to import all Routes in all Apps")
        for backend, config in backends.items():
            discover_from_config(config, backend, type=ROUTER_TYPE, catalog=catalog, register = register,)

    setDiscover(False)
    # The Registry we return holds all information of the registered Nodes according to their backend
    return get_registry()
