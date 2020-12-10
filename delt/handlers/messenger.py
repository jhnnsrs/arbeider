
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Messenger(object):

    def __init__(self, channel, layer=get_channel_layer()) -> None:#
        self.channel = channel
        self.layer = layer

    def contact(self, function: str, message: str, serializer = None):
        if serializer: message = serializer(message).data
        async_to_sync(self.layer.send)(self.channel,{"type": function, "data": message})

