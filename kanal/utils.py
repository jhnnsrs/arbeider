
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


channel_layer = get_channel_layer()



def layer_send(channel, method, layer=channel_layer):
    return lambda x: async_to_sync(channel_layer.send)(channel,{"type": method, "data" : x})