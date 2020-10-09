from konfig.node import Konfig
from konfig.params import Inputs, Outputs, ModelPort, IntPort
from elements.models import Representation


class DeepLearningOutputs(Outputs):
    outputrep = ModelPort(Representation, description="The Outgoing Representation")

class DeepLearningInputs(Inputs):
    firstrep = ModelPort(Representation, description="The Microscopic Dataset that is going to be parsed", primary=True)
    secondrep = ModelPort(Representation, description="The Microscopic Dataset that is going to be parsed together with the first one", primary=True)
    

class DeepLearningKonfig(Konfig):
    inputs = DeepLearningInputs
    outputs = DeepLearningOutputs





