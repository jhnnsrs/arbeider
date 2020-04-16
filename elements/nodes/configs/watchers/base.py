from fremmed.models import FrontendNode
from delt.params import Inputs,Outputs
from delt.node import NodeConfig

class BaseWatcherInputs(Inputs):
    pass

class BaseWatcherOutputs(Outputs):
    pass


class BaseWatcherConfig(NodeConfig):
    register = FrontendNode
    package = "@canonical/elements"
    variety = "watcher"