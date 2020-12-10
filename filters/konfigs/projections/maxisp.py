from konfig.widgets import SliderQueryWidget
from konfig.params import ObjectPort, IntPort
from .base import BaseProjectorOutputs, BaseProjectorConfig, BaseProjectorInputs


PlanesWiget = SliderQueryWidget(query= """query {
  data: dimsof(rep: {{rep}}){
    max: z
  }
}""", dependencies=["rep"])






class Slice(ObjectPort):
    """ A Slice is an Extension of a Lower and Upper Item"""
    upper = IntPort(allow_null=True, help_text="The Upper Index / The Upper Limit for the Slice", widget=PlanesWiget)
    lower = IntPort(allow_null=True, help_text="The Lower Index / The Lower Limit for the Slice", widget=PlanesWiget)

class MaxISPInputs(BaseProjectorInputs):
    slice = Slice(allow_null=True)

class MaxISPConfig(BaseProjectorConfig):
    """This is a Maximum Intensity Projection

    Does a Maximum Projection of the Incoming Array
    Longer class information....

    """
    name = "Maximum Intensity Projection"
    variety = "projector"
    interface = "maxisp"
    inputs = MaxISPInputs
    outputs = BaseProjectorOutputs