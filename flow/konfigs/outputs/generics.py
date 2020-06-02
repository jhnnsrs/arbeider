from konfig.node import Konfig
from konfig.params import CharField, IntField, Inputs, Outputs


class GenericOutputKonfig(Konfig):
    package = "@flow/outputs/generics"
    variety = "output"



class IntInput(Inputs):
    int = IntField(label="Integer", description="The Output Integer")

class IntOutput(Outputs):
    pass

class IntOutputKonfig(GenericOutputKonfig):
    interface = "int"
    inputs = IntInput
    outputs = IntOutput


class StrInput(Inputs):
    str = CharField(label="String", description="The Input Characters")

class StrOutput(Outputs):
    pass


class StrOutputKonfig(GenericOutputKonfig):
    interface = "str"
    inputs = StrInput
    outputs = StrOutput