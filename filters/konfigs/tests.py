from konfig.params import BoolField, Inputs, IntField, ModelField, Outputs
from elements.models import ROI, Representation
from elements.serializers import RepresentationSerializer
from konfig.node import Konfig


class TestInputs(Inputs):
    rep = ModelField(Representation, label="Representation", help_text="The Representation that will be projected")
    roi = ModelField(ROI, label="Representation", help_text="The Representation that will be projected")

class TestOutputs(Outputs):
    rep = ModelField(Representation, label="Representation", help_text="The Outgoing Representation (with altered dimensions)")


class TestConfig(Konfig):
    package = "@canoncial/generic/testers"
    interface = "tester"
    inputs = TestInputs
    outputs = TestOutputs
    variety = "projector"