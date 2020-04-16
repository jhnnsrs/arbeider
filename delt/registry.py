class RegistryError(Exception):
    pass



class Registry():
    """This is the bases In Memory Registry Class that registeres every Node in Memory
    """

    def __init__(self):
        self.channelConsumersMap = {}
        self.nodeidentifierBackendMap = {}
        self.nodes = {}
        self.viewsetRoutes = {}
        self.nodeIdentifierPublishersMap = {}

    def getConsumersMap(self):
        return self.channelConsumersMap

    def getViewsetRoutes(self):
        return self.viewsetRoutes

    def registerChannelConsumer(self,channel: str, consumer):
        """ The channel you want to register too """
        if channel in self.channelConsumersMap:
            raise RegistryError(" Channel already registered. Configuration Error!")
        else:
            self.channelConsumersMap[channel] = consumer

    def registerViewsetRoute(self,basename: str, route):
        """ The channel you want to register too """
        if basename in self.viewsetRoutes:
            oldviewset = self.viewsetRoutes[basename]["viewset"].__name__
            newviewset = route["viewset"].__name__



            raise RegistryError(f" Basename {basename} already registered. Configuration Error! Was registered to {oldviewset}, {newviewset} wants to Register")
        else:
            self.viewsetRoutes[basename] = route



    def registerBackendForNode(self, nodeidentifier, backend):
        if nodeidentifier in self.nodeidentifierBackendMap:
            raise RegistryError(" Node already registered with other Backend. Configuration Error!")
        else:
            self.nodeidentifierBackendMap[nodeidentifier] = backend


    def getBackendForNode(self, nodeidentifier):
        if nodeidentifier in self.nodeidentifierBackendMap:
            return self.nodeidentifierBackendMap[nodeidentifier]
        else:
            raise RegistryError("Node not registered with any Backend. Did you overide NodeBackend?")
        



GLOBAL_REGISTRY = Registry()

def get_registry():
    return GLOBAL_REGISTRY