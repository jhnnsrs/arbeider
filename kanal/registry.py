import logging


logger = logging.getLogger(__name__)


class RegistryError(Exception):
    pass



class KanalRegistry():
    """This is the bases In Memory Registry Class that registeres every Node in Memory
    """

    def __init__(self):
        self.channelConsumersMap = {}
        self.nodeidentifierBackendMap = {}
        self.nodeidentifierConfigMap = {}
        self.nodes = {}
        self.viewsetRoutes = {}
        self.nodeIdentifierPublishersMap = {}

    def getConsumersMap(self):
        return self.channelConsumersMap

    def registerChannelConsumer(self,channel: str, consumer):
        """ The channel you want to register too """
        if channel in self.channelConsumersMap:
            raise RegistryError(" Channel already registered. Configuration Error!")
        else:
            logger.info("Registering Consumer for channel {channel}")
            self.channelConsumersMap[channel] = consumer


    def registerConfigForIdentifier(self, nodeidentifier, config):
        if nodeidentifier in self.nodeidentifierConfigMap:
            raise RegistryError(" Nodeidentifier already registered. Configuration Error!")
        else:
            self.nodeidentifierConfigMap[nodeidentifier] = config

    def getConfigForIdentifier(self, nodeidentifier):
        if nodeidentifier in self.nodeidentifierConfigMap:
            return self.nodeidentifierConfigMap[nodeidentifier]
        else:
            raise RegistryError("Node not registered with any Config. Did you overide NodeBackend?")
        



kanal_registry = None

def get_kanal_registry():
    global kanal_registry
    if kanal_registry is None:
        kanal_registry = KanalRegistry()
    return kanal_registry





