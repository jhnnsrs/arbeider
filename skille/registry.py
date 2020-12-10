from delt.registries.registry import get_registry_registry
from delt.registries.additionals import get_additionals_registry
from delt.handlers.newbase import BaseHandler


registry = None

class SkilleRegistry():

    def __init__(self) -> None:
        self.identifierHandlerMap: dict[str, BaseHandler] = {}

    def registerGraphWorker(self, function):

        


        identifier = handler.env.getProviderName()
        self.identifierHandlerMap[identifier] = handler

    def getConsumerMap(self):
        channelMap = { handler.env.getChannelChannelName(): handler.getChannel().as_asgi() for _, handler in self.identifierHandlerMap.items()}
        gatewayMap = { handler.env.getGatewayChannelName(): handler.getGateway().as_asgi() for _, handler in self.identifierHandlerMap.items()}

        return {**channelMap, **gatewayMap}

    def getHandler(self, identifier):
        return self.identifierHandlerMap[identifier]




def get_skille_registry() -> SkilleRegistry:
    global registry
    if registry is None:
        registry = SkilleRegistry() # We are registering this app always
        get_registry_registry().registerRegistry(registry)
    return registry

