import hashlib
import re
import uuid

from django.conf import settings
from rest_framework import serializers

from delt.params import CharField
from delt.settingsregistry import get_settings_registry

# Pod Selector Settings
ANYSELECTOR = "__any__"
UNIQUESELECTOR = "#"
PROVIDERSELECTOR = "@"
SEPERATOR = "/"


# Statuscodes

PODACTIVE = "active"
PODREADY = "active"
PODFAILED = "failed"
PODBUSY = "budy"
PODPENDING = "pending"



def pod_identifier(package, interface, provider,  withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    hash = hashlib.sha1()
    salt = package + interface + provider + withsecret
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()


