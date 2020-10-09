from delt.integrity import node_identifier
import hashlib
import logging

from django.conf import settings
from rest_framework.fields import empty

from konfig.utils import parse_inputs, parse_outputs
from konfig.params import DummyInputs, DummyOutputs
from delt.models import Node

logger = logging.getLogger(__name__)




class Konfig(object):
    register = None
    inputs = DummyInputs
    outputs = DummyOutputs
    package = None
    interface = None
    description = None
    nodeclass = None
    name = None
    variety = None

    def __init__(self):
        if issubclass(self.inputs, DummyInputs):
            logger.warning("This Job has Dummy Arguments")
        if issubclass(self.outputs, DummyOutputs):
            logger.warning("This Job has Dummy Settings")
        super().__init__()

    @classmethod
    def get_package(cls):
        return cls.package or cls.__module__;

    @classmethod
    def get_interface(cls):
        return cls.interface or cls.__name__;

    @classmethod
    def get_node_identifier(cls):
        return node_identifier(cls.get_package(), cls.get_interface())

    @classmethod
    def get_node(cls):
        return Node.objects.get(identifier=cls.get_node_identifier())

    @classmethod
    def serialize(cls):
        return {
            "name" : cls.name or cls.__name__,
            "inputs": parse_inputs(cls),
            "outputs": parse_outputs(cls),
            "package": cls.get_package(),
            "interface": cls.get_interface(),
            "variety": cls.variety or "default",
            "description": cls.description or cls.__doc__ or "No Description",
            "nodeclass": cls.nodeclass or "konfig-node"
        }
