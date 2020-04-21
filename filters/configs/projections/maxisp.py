from delt.params import Object, IntField
from .base import BaseProjectorOutputs, BaseProjectorConfig, BaseProjectorInputs

class Slice(Object):
    upper = IntField(allow_null=True, help_text="The Upper Index / The Upper Limit for the Slice")
    lower = IntField(allow_null=True, help_text="The Lower Index / The Lower Limit for the Slice")

class MaxISPInputs(BaseProjectorInputs):
    slice = Slice()

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