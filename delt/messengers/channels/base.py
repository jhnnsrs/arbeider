from delt.messengers.base import BaseMessenger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from inspect import iscoroutinefunction
import logging


logger = logging.getLogger(__name__)




class BaseChannelMessenger(BaseMessenger):
    routing = None
    serializer = None
    pack = "data"

    def __init__(self, routing, layer=get_channel_layer()) -> None:
        self.layer = layer
        super.__init__(routing)

    def contact(self, function: str, data: str, serializer = None):
        serializer = serializer or self.serializer
        if self.pack: 
            message = {}
            message[self.pack] = data
        else:
            message = data
        
        if serializer: message = serializer(message).data
        async_to_sync(self.layer.send)(self.routing,{"type": function, "data": message})

    
    def receive(self, serializer = None,  raise_exception=True, colapse=None):
        serializer = serializer or self.serializer
        
        def real_decorator(function):


            def wrapper(cls, message):
                logger.info("Called Synchroniously")
                serialized = serializer(data=message["data"])
                if serialized.is_valid(raise_exception=raise_exception):
                    data = serialized.validated_data
                    if self.pack: data = data[self.pack]
                    function(cls, data)


            async def async_wrapper(cls, message):
                logger.info("Called Asynchronously")

                def get_data_from_message(message):
                    serialized = serializer(data=message["data"])
                    if serialized.is_valid(raise_exception=raise_exception):
                        data = serialized.validated_data
                        if self.pack: data = data[self.pack]
                        return data
                
                
                data = await sync_to_async(get_data_from_message)(message)
                return await function(cls, data)

            return async_wrapper if iscoroutinefunction(function) else wrapper

        return real_decorator