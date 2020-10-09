from rest_framework import serializers

from konfig import params
from konfig.node import Konfig
from drawing.models import LineRoi
from elements.models import ROI, Representation


class Vectors(params.ObjectPort):
    x = params.ListPort(child=params.FloatPort())
    y = params.ListPort(child=params.FloatPort())

class DrawerInputs(params.Inputs):
    rep = params.ModelPort(Representation, primary=True)
    roi = params.ModelPort(ROI, primary=True)

class DrawerOutputs(params.Outputs):
    vectors = Vectors()


class DrawerConfig(Konfig):
    package = "@canonical/drawing"
    variety = "drawer"
    name="Drawer"
    interface = "drawer"
    inputs = DrawerInputs
    outputs = DrawerOutputs