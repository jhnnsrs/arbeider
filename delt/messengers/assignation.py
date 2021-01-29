
from inspect import iscoroutinefunction
from delt.messengers.base import BaseMessenger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from delt.serializers import AssignationMessageSerializer

class AssignationMessenger(BaseMessenger):
    channel = None
    serializer = AssignationMessageSerializer
    pack = "assignation"


    def __init__(self, channel, layer=get_channel_layer()) -> None:#
        self.channel = channel or self.channel
        self.layer = layer

    def contact(self, function: str, data: str, serializer = None):
        serializer = serializer or self.serializer
        if self.pack: 
            message = {}
            message[self.pack] = data
        else:
            message = data
        
        if serializer: message = serializer(message).data
        async_to_sync(self.layer.send)(self.channel,{"type": function, "data": message})


    def receive(self, serializer = None,  raise_exception=True):
        serializer = serializer or self.serializer
        

        def real_decorator(function):


            def wrapper(cls, message):
                print("CALLED SYNC")
                serialized = serializer(data=message["data"])
                if serialized.is_valid(raise_exception=raise_exception):
                    data = serialized.validated_data
                    if self.pack: data = data[self.pack]
                    function(cls, data)


            async def async_wrapper(cls, message):
                print("CALLED ASYNC")

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

    
