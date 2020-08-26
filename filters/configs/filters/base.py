from delt.node import NodeConfig
from delt.params import BoolField, Inputs, IntField, ModelField, Outputs
from elements.models import Representation
from elements.serializers import RepresentationSerializer
from konfig.node import Konfig


class BaseFilterInputs(Inputs):
    rep = ModelField(Representation, info="The Incoming Representation", description="This Representation will be <b>filtered</b>", label="Representation")

class BaseFilterOutputs(Outputs):
    rep = ModelField(Representation, info="The Outgoing Representation", description="The Representation that was be <b>filtered</b>", label="Representation")


class BaseFilterKonfig(Konfig):
    package = "@canoncial/generic/filters"
    inputs = BaseFilterInputs
    outputs = BaseFilterOutputs
    variety = "filter"