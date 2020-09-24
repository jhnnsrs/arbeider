from delt.validators.base import BaseValidator, BaseValidatorSettings
from konfig.node import Konfig

class KonfigValidatorSettings(BaseValidatorSettings):
    provider = "config"


class KonfigValidator(BaseValidator):
    settings = KonfigValidatorSettings()

    def __init__(self, konfig: Konfig):
        self.konfig = konfig
        super().__init__()


    def validateInputs(self, inputs) -> dict:
        serialized = self.konfig.inputs(data=inputs)
        if serialized.is_valid(raise_exception=True):
            return serialized.validated_data

    def validateOutputs(self, outputs) -> dict:
        serialized = self.konfig.inputs(data=outputs)
        if serialized.is_valid(raise_exception=True):
            return serialized.validated_data