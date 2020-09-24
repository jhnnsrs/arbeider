from rest_framework import serializers

from konfig import params
from konfig.node import Konfig
from drawing.models import LineRoi
from elements.models import ROI, Representation


class Vectors(params.Object):
    x = params.ListField(child=params.FloatField())
    y = params.ListField(child=params.FloatField())

class DrawerInputs(params.Inputs):
    rep = params.ModelField(Representation)

class DrawerOutputs(params.Outputs):
    vectors = Vectors()


class DrawerConfig(Konfig):
    package = "@canonical/drawing"
    variety = "drawer"
    name="Drawer"
    interface = "drawer"
    inputs = DrawerInputs
    outputs = DrawerOutputs