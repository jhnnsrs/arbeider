from delt.node import NodeConfig
from delt.params import BoolField, Inputs, IntField, ModelField, Outputs
from elements.models import Representation
from elements.serializers import RepresentationSerializer
from konfig.node import Konfig


class BaseFilterInputs(Inputs):
    rep = ModelField(Representation, info="The Incoming Representation", description="This Representation will be <b>filtered</b>", label="Representation")

class BaseFilterOutputs(Outputs):
    rep = RepresentationSerializer(help_text="The Outgoing Representation (with altered dimensions)", label="Representation")


class BaseFilterConfig(Konfig):
    package = "@canoncial/generic/filters"
    inputs = BaseFilterInputs
    outputs = BaseFilterOutputs
    variety = "filter"