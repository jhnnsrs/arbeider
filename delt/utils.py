from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import inspect
import logging
import namegenerator


channel_layer = get_channel_layer()

def props(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not inspect.ismethod(value):
            pr[name] = value
    return pr

logger = logging.getLogger(__name__)

def pipe(event="pipe"):

    def real_decorator(function):

        def wrapper(*args, **kwargs):
            logger.info(f"Pipe: {event} called with {args} and {kwargs}")
            return function(*args, **kwargs)
        return wrapper

    return real_decorator


def compareNodes(node1, params: dict ):
    excluded_keys = 'created', '_state', 'timestamp', 'user', 'uid', 'changed' #Example. Modify to your likings.
    d1, d2 = node1.__dict__, params
    old, new = {}, {}
    for k,v in d1.items():
        if k in excluded_keys:
            continue
        try:
            if v != d2[k]:
                old.update({k: v})
                new.update({k: d2[k]})
        except KeyError:
            old.update({k: v})
    
    return new



def channel_layer_send(channel, method, layer = channel_layer):
    return lambda x: async_to_sync(layer.send)(channel,{"type": method, "data" : x})

def gateway_send(method):
    return channel_layer_send("gateway", method)



def generate_random_name():
    return namegenerator.gen()