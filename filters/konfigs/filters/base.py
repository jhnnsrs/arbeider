from konfig.params import  Inputs, ModelPort, Outputs
from elements.models import Representation
from elements.serializers import RepresentationSerializer
from konfig.node import Konfig


class BaseFilterInputs(Inputs):
    rep = ModelPort(Representation, description="The Incoming Representation", label="Representation", primary=True)

class BaseFilterOutputs(Outputs):
    rep = ModelPort(Representation, description="The Outgoing Representation", label="Representation")


class BaseFilterKonfig(Konfig):
    package = "@canoncial/generic/filters"
    inputs = BaseFilterInputs
    outputs = BaseFilterOutputs
    variety = "filter"