from konfig.params import BoolField, Inputs, IntField, ModelField, Outputs
from elements.models import Representation
from elements.serializers import RepresentationSerializer
from konfig.node import Konfig


class BaseProjectorInputs(Inputs):
    rep = ModelField(Representation, label="Representation", help_text="The Representation that will be projected")

class BaseProjectorOutputs(Outputs):
    rep = ModelField(Representation, label="Representation", help_text="The Outgoing Representation (with altered dimensions)")


class BaseProjectorConfig(Konfig):
    package = "@canoncial/generic/projectors"
    inputs = BaseProjectorInputs
    outputs = BaseProjectorOutputs
    variety = "projector"