from delt.validators.base import BaseValidator, BaseValidatorSettings
from delt.node import NodeConfig

class AlwaysTrueValidatorSettings(BaseValidatorSettings):
    provider = "allwaystrue"


class AlwaysTrueValidator(BaseValidator):
    settings = AlwaysTrueValidatorSettings()

    def validateInputs(self, inputs) -> dict:
        return True

    def validateOutputs(self, outputs) -> dict:
        return True