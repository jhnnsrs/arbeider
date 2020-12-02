from vart.handler import Handler


registry = None

class HandlerRegistry():

    def __init__(self) -> None:
        self.identifierHandlerMap: dict[str, Handler] = {}

    def registerHandler(self, identifier: str, handler: Handler):
        self.identifierHandlerMap[identifier] = handler

    def getConsumerMap(self):
        channelMap = { handler.settings.channel_channel: handler.getChannel().as_asgi() for _, handler in self.identifierHandlerMap.items()}
        gatewayMap = { handler.settings.gateway_channel: handler.getGateway().as_asgi() for _, handler in self.identifierHandlerMap.items()}

        return {**channelMap, **gatewayMap}

    def getHandler(self, identifier):
        return self.identifierHandlerMap[identifier]




def get_handler_registry() -> HandlerRegistry:
    global registry
    if registry is None:
        registry = HandlerRegistry()
    return registry