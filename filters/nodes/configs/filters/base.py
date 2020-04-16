from delt.params import (BoolField, Inputs, IntField, ModelField,
                         Outputs)
from delt.node import NodeConfig
from elements.models import Representation

class BaseFilterInputs(Inputs):
    rep = ModelField(Representation, help_text="The Representation that will be filtered", label="Representation")

class BaseFilterOutputs(Outputs):
    rep = ModelField(Representation, help_text="The Outgoing Representation (with altered dimensions)", label="Representation")


class BaseFilterConfig(NodeConfig):
    package = "@canoncial/generic/filters"
    inputs = BaseFilterInputs
    outputs = BaseFilterOutputs