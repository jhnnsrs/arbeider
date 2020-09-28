from konfig.params import  Inputs, ModelField, Outputs
from elements.models import Representation
from elements.serializers import RepresentationSerializer
from konfig.node import Konfig


class BaseFilterInputs(Inputs):
    rep = ModelField(Representation, description="The Incoming Representation", label="Representation", primary=True)

class BaseFilterOutputs(Outputs):
    rep = ModelField(Representation, description="The Outgoing Representation", label="Representation")


class BaseFilterKonfig(Konfig):
    package = "@canoncial/generic/filters"
    inputs = BaseFilterInputs
    outputs = BaseFilterOutputs
    variety = "filter"