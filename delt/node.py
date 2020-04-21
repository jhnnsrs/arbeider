import hashlib
import logging

from django.conf import settings
from rest_framework.fields import empty

from delt.params import DummyInputs, DummyOutputs

logger = logging.getLogger(__name__)

def node_identifier(package, interface, withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    hash = hashlib.sha1()
    salt = package + interface + withsecret
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()


class NodeConfig(object):
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

    def get_identifier_for_backend(self, backend):
        return node_identifier(self.package, self.interface, backend)