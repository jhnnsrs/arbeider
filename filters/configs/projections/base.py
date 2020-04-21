from delt.params import (BoolField, Inputs, IntField, ModelField,
                         Outputs)
from delt.node import NodeConfig
from elements.models import Representation

class BaseProjectorInputs(Inputs):
    rep = ModelField(Representation, help_text="The Representation that will be projected")

class BaseProjectorOutputs(Outputs):
    rep = ModelField(Representation, help_text="The Outgoing Representation (with altered dimensions)")


class BaseProjectorConfig(NodeConfig):
    package = "@canoncial/generic/projectors"
    inputs = BaseProjectorInputs
    outputs = BaseProjectorOutputs
    variety = "projector"