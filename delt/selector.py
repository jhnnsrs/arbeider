from delt.handlers.base import BaseHandler
from delt.settingsregistry import get_settings_registry
import re

# The Backend Selector

provider = re.compile(r'@(?P<provider>[a-z]*)/(?P<substring>.*)')

#subhandlers
unique_handler = re.compile(r'__unique__')
all_handler = re.compile(r'__all__')
new_handler = re.compile(r'__new__')
id_handler = re.compile(r'#(?P<id>[a-z0-9A-Z]*)')


#Helpers
unique = lambda selector: True if unique_handler.match(selector) else False
all =  lambda selector: True if all_handler.match(selector) else False
new =  lambda selector: True if new_handler.match(selector) else False
id = lambda selector: id_handler.match(selector).group("id") if id_handler.match(selector) else False

def get_handler_for_selector(selector: str) -> BaseHandler:

    m = provider.match(selector)
    if m:
        return get_settings_registry().getHandlerForProvider(m.group("provider"))

def get_provider_for_selector(selector: str) -> BaseHandler:

    m = provider.match(selector)
    if m:
        return m.group("provider"), m.group("substring")
    else:
        raise Exception("We didnt find any provider matching")#