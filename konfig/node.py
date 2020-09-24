import hashlib
import logging

from django.conf import settings
from rest_framework.fields import empty

from konfig.params import DummyInputs, DummyOutputs
from delt.models import Node

logger = logging.getLogger(__name__)

def node_identifier(package, interface, withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    hash = hashlib.sha1()
    salt = package + interface + withsecret
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()


class Konfig(object):
    register = None
    inputs = DummyInputs
    outputs = DummyOutputs
    package = None
    interface = None

    def __init__(self):
        if issubclass(self.inputs, DummyInputs):
            logger.warning("This Job has Dummy Arguments")
        if issubclass(self.outputs, DummyOutputs):
            logger.warning("This Job has Dummy Settings")
        super().__init__()

    @classmethod
    def get_node_identifier(cls):
        return node_identifier(cls.package, cls.interface,)

    @classmethod
    def get_node(cls):
        return Node.objects.get(identifier=cls.get_node_identifier())
