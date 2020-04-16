from delt.params import Arguments, BoolField, IntField, ModelField, Returns, JobHelper, Settings
from elements.models import Representation, ROI


class TestArgs(Arguments):
    rep_one = ModelField(Representation, help_text="The Representation that will be appended to")
    rep_two = ModelField(Representation, help_text="The Representation that will be appended")

class TestReturns(Returns):
    rep = ModelField(Representation, help_text="The Outgoing Representation")
    roi = ModelField(ROI, help_text="The Outgoing ROI")

class TestSettings(Settings):
    sigma = IntField()
    retry = BoolField()

class Testing(JobHelper):
    args = TestArgs()
    settings = TestSettings()
    returns  = TestSettings()
    pass