
class RegistryError(Exception):
    pass


class SettingRegistry():

    def __init__(self):
        #TODO Set this lazyliy from the Settings
        self.providerHandlerMap = {}
        self.publisherHandlerMap = {}
        self.backendHandlerMap = {}

    def getHandlers(self):
        return self.providerHandlerMap
    

    def setHandlerForProvider(self, provider, handler):
        if provider in self.providerHandlerMap:
            pass
            #raise RegistryError(" Backend already registered with another Handler. Configuration Error!")
        else:
            self.providerHandlerMap[provider] = handler
 
    def getHandlerForProvider(self, provider):
        if provider in self.providerHandlerMap:
            return self.providerHandlerMap[provider]
        else:
            raise RegistryError("No Handler registered with Provider. Did you register it?")

    def getPublishersForEvent(self, event):
        publishers = []
        for provider, publisher in self.publisherHandlerMap.items():
            if event in publisher.settings.fields or publisher.settings.onall:
                publishers.append(publisher)
        return publishers

    def getPublisher(self, publisher):
        if publisher in self.publisherHandlerMap:
            return self.publisherHandlerMap[publisher]
        else:
            raise RegistryError(f"No Handler registered with Publisher {publisher}. Did you register it?")


    def setPublisher(self, publisher, handler):
        if publisher in self.publisherHandlerMap:
            pass
            #raise RegistryError(" Publisher already registered with another Handler. Configuration Error!")
        else:
            self.publisherHandlerMap[publisher] = handler

    def setNodeBackend(self, backend, nodebackend):
        if backend in self.backendHandlerMap:
            raise RegistryError(" Backend already registered with another Handler. Configuration Error!")
        else:
            self.backendHandlerMap[backend] = nodebackend



GLOBAL_SETTINGS_REGISTRY = SettingRegistry()

def get_settings_registry()-> SettingRegistry:
    return GLOBAL_SETTINGS_REGISTRY
