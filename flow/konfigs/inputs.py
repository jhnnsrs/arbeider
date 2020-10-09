from rest_framework import serializers
from elements.models import Representation
from konfig.node import Konfig
from konfig.params import ModelPort, Inputs, Outputs

class ModelInputKonfig(Konfig):
    package = "@flow/inputs/model"
    variety = "input"


class RepresentationInput(Inputs):
    pass

class RepresentationOutput(Outputs):
    rep = ModelPort(Representation, label="The Representation", description="This will be the right thing")


class RepresentationInputKonfig(ModelInputKonfig):
    interface = "representation"
    inputs = RepresentationInput
    outputs = RepresentationOutput