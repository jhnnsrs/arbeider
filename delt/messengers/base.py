
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from abc import ABC, abstractmethod

class BaseMessenger:
    """
    Messengers take care of asynchronous scheduling of Tasks
    """
    routing = None
    pack = "data"

    def __init__(self, routing) -> None:#
        self.routing = routing or self.routing

    @abstractmethod
    def contact(self, function: str, data: str, serializer = None):
        pass

    @abstractmethod
    def receive(self, serializer = None,  raise_exception=True, colapse=None):
        pass
        