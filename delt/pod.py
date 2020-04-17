import uuid

from rest_framework import serializers
from delt.params import CharField


class DummyPod(object):
    pass


ANYSELECTOR = "any"
UNIQUESELECTOR = "unique"

UNIQUEIDENTIFIER = "unique"
SEPERATOR = "/"
class Selector(object):
    type = ANYSELECTOR
    params = None

    def __init__(self, selectorstr: str):
        if selectorstr.startswith(UNIQUEIDENTIFIER):
            self.type = UNIQUESELECTOR
            internal = f"{UNIQUEIDENTIFIER}{SEPERATOR}"
            if selectorstr.startswith(internal):
                self.params = selectorstr.split(internal)[1]

        
        super().__init__()