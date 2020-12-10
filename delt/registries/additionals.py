from delt.registries.registry import BaseRegistry
from delt.handlers.newbase import BaseHandler
from channels.consumer import SyncConsumer

additionalregistry = None

class AdditionalsRegistry(BaseRegistry):

    def __init__(self) -> None:
        self.identifierConsumerMap: dict[str, SyncConsumer] = {}
        self.identifierAppMap: dict[str, str] = {}

    def registerConsumer(self, app: str, identifier: str, consumer: SyncConsumer):
        """Registers Consumer for App in the Additional Registry

        Args:
            app (str): A Unique App identifier
            identifier (str): A unique Channel identifier (used for communication with Channel backend)
            consumer (SyncConsumer): The consumer you want to Register
        """
        self.identifierConsumerMap[identifier] = consumer
        self.identifierAppMap[identifier] = app

    def getConsumerMap(self, exclude=None, include=None) -> dict:
        """Gets the consumers stored in the Registry

        Args:
            exclude ([type], optional): Apps to be excluded. Defaults to None.
            include ([type], optional): Apps to be included. Defaults to None.

        Returns:
            dict: The Consumers
        """
        initialMap = { identifier: consumer.as_asgi() for identifier, consumer in self.identifierConsumerMap.items()}
        if include:
            return { identifier: consumer for identifier, consumer in self.identifierConsumerMap.items() if identifier in include}
        if exclude:
            return { identifier: consumer for identifier, consumer in self.identifierConsumerMap.items() if identifier not in exclude}
        
        return initialMap





def get_additionals_registry() -> AdditionalsRegistry:
    global additionalregistry
    if additionalregistry is None:
        additionalregistry = AdditionalsRegistry()
    return additionalregistry