import uuid
import hashlib
from django.conf import settings
from rest_framework import serializers
from delt.params import CharField


class DummyPod(object):
    pass


ANYSELECTOR = "any"
UNIQUESELECTOR = "unique"

UNIQUEIDENTIFIER = "unique"
SEPERATOR = "/"


def pod_identifier(package, interface, provider,  withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    hash = hashlib.sha1()
    salt = package + interface + provider + withsecret
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()




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