from delt import params
from konfig.node import Konfig
from drawing.models import LineRoi
from drawing.configs.drawer import Vectors
from elements.models import ROI, Representation


class LinerInputs(params.Inputs):
    vectors = Vectors()

class LinerOutputs(params.Outputs):
    roi = params.ModelField(LineRoi)


class LinerKonfig(Konfig):
    package = "@canonical/drawing"
    variety = "liner"
    name="Liner"
    interface = "liner"
    inputs = LinerInputs
    outputs = LinerOutputs