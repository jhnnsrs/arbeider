from delt.registries.registry import BaseRegistry
from delt.handlers.newbase import BaseHandler


handlerregistry = None

class HandlerRegistry(BaseRegistry):

    def __init__(self) -> None:
        self.identifierHandlerMap: dict[str, BaseHandler] = {}

    def registerHandler(self,handler: BaseHandler):
        identifier = handler.env.getProviderName()
        self.identifierHandlerMap[identifier] = handler

    def getConsumerMap(self):
        channelMap = { handler.env.getChannelChannelName(): handler.getChannel().as_asgi() for _, handler in self.identifierHandlerMap.items()}
        gatewayMap = { handler.env.getGatewayChannelName(): handler.getGateway().as_asgi() for _, handler in self.identifierHandlerMap.items()}

        return {**channelMap, **gatewayMap}

    def getHandler(self, identifier):
        return self.identifierHandlerMap[identifier]


    def getHandlerForProvider(self, provider):
        return self.getHandler(provider.name)




def get_handler_registry() -> HandlerRegistry:
    global handlerregistry
    if handlerregistry is None:
        handlerregistry = HandlerRegistry()
    return handlerregistry