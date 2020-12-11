from delt.registries.registry import BaseRegistry
from delt.handlers.newbase import BaseHandler


widgetregistry = None

class WidgetRegistry(BaseRegistry):

    def __init__(self) -> None:
        self.widgetNameWidgetMap: dict[str, BaseHandler] = {}

    def registerWidget(self,widget):
        name = widget.__name__
        self.widgetNameWidgetMap[name] = widget

    def getConsumerMap(self):
        channelMap = { handler.env.getChannelChannelName(): handler.getChannel().as_asgi() for _, handler in self.identifierHandlerMap.items()}
        gatewayMap = { handler.env.getGatewayChannelName(): handler.getGateway().as_asgi() for _, handler in self.identifierHandlerMap.items()}

        return {**channelMap, **gatewayMap}

    def getHandler(self, identifier):
        return self.identifierHandlerMap[identifier]




def get_widget_registry() -> WidgetRegistry:
    global widgetregistry
    if widgetregistry is None:
        widgetregistry = WidgetRegistry()
    return widgetregistry



