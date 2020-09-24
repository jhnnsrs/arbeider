from elements.models import Representation
from konfig.node import Konfig
from konfig.params import ModelField, Inputs, Outputs

class ModelOutputKonfig(Konfig):
    package = "@flow/ouputs/model"
    variety = "output"


class RepresentationInput(Inputs):
    rep = ModelField(Representation, label="The Representation", description="This will be the right thing")

class RepresentationOutput(Outputs):
    pass


class RepresentationOutputKonfig(ModelOutputKonfig):
    interface = "representation"
    inputs = RepresentationInput
    outputs = RepresentationOutput