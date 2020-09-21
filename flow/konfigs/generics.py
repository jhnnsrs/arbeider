from konfig.node import Konfig
from konfig.params import CharField, IntField, Inputs, Outputs


class GenericInputKonfig(Konfig):
    package = "@flow/inputs/generics"
    variety = "input"



class IntInput(Inputs):
    pass

class IntOutput(Outputs):
    int = IntField(label="Integer", description="The Input Integer")


class IntInputKonfig(GenericInputKonfig):
    interface = "int"
    inputs = IntInput
    outputs = IntOutput


class StrInput(Inputs):
    pass

class StrOutput(Outputs):
    str = CharField(label="String", description="The Input Characters")


class StrInputKonfig(GenericInputKonfig):
    interface = "str"
    inputs = StrInput
    outputs = StrOutput