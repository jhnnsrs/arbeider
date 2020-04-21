import graphene
from PIL.Image import NONE

from delt.node import NodeConfig


class to_object(object):
    config: NodeConfig = None

    def __init__(self, config: NodeConfig):

        self.config = config

    def __call__(self, cls):
        # Do Initial Weird stuff to class
        fields = {"hallo": {"entity": graphene.String(), "resolver" : lambda self, info, **kwargs: "Hallo"}}

        for key, value in fields.items():
            setattr(cls, key, value["entity"])
            setattr(cls, "resolve_"+key, value["resolver"])

        return cls
        

class register_with_schema(to_object):
    pass