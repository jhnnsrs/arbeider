from delt.validators.base import BaseValidator, BaseValidatorSettings
from delt.node import NodeConfig

class ConfigValidatorSettings(BaseValidatorSettings):
    provider = "config"


class ConfigValidator(BaseValidator):
    settings = ConfigValidatorSettings()

    def __init__(self, config: NodeConfig):
        self.config = config
        super().__init__()


    def validateInputs(self, inputs) -> dict:
        serialized = self.config.inputs(data=inputs)
        if serialized.is_valid(raise_exception=True):
            return serialized.validated_data

    def validateOutputs(self, outputs) -> dict:
        serialized = self.config.inputs(data=outputs)
        if serialized.is_valid(raise_exception=True):
            return serialized.validated_data