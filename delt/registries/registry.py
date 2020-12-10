




from delt.registries.base import BaseRegistry
import collections

registryregistry = None

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

class RegistryRegistry():

    def __init__(self) -> None:
        self.appRegistryMap: dict[str, BaseRegistry] = {}

    def getConsumerMap(self):
        channelMap = { app: registry.getConsumerMap() for app, registry in self.appRegistryMap.items()}
        return flatten(channelMap)





def get_registry_registry() -> RegistryRegistry:
    global registryregistry
    if registryregistry is None:
        registryregistry = RegistryRegistry()
    return registryregistry