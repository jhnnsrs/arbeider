from konfig.params import BoolPort, Inputs, IntPort, ModelPort, Outputs
from elements.models import Representation
from elements.serializers import RepresentationSerializer
from konfig.node import Konfig


class BaseProjectorInputs(Inputs):
    rep = ModelPort(Representation, label="Representation", help_text="The Representation that will be projected")

class BaseProjectorOutputs(Outputs):
    rep = ModelPort(Representation, label="Representation", help_text="The Outgoing Representation (with altered dimensions)")


class BaseProjectorConfig(Konfig):
    package = "@canoncial/generic/projectors"
    inputs = BaseProjectorInputs
    outputs = BaseProjectorOutputs
    variety = "projector"