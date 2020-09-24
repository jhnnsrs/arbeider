from konfig.node import Konfig
from konfig.params import Inputs, Outputs, ModelField, IntField
from elements.models import Representation


class DeepLearningOutputs(Outputs):
    outputrep = ModelField(Representation, description="The Outgoing Representation")

class DeepLearningInputs(Inputs):
    firstrep = ModelField(Representation, description="The Microscopic Dataset that is going to be parsed", primary=True)
    secondrep = ModelField(Representation, description="The Microscopic Dataset that is going to be parsed together with the first one", primary=True)
    

class DeepLearningKonfig(Konfig):
    inputs = DeepLearningInputs
    outputs = DeepLearningOutputs





