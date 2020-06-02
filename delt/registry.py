class RegistryError(Exception):
    pass



class Registry():
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
        



registry = None

def get_registry():
    global registry
    if registry is None:
        registry = Registry()
    return registry



def get_delt_registry():
    return get_registry()




