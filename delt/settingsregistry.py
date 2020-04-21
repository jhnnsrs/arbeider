
class RegistryError(Exception):
    pass


class SettingRegistry():

    def __init__(self):
        #TODO Set this lazyliy from the Settings
        self.backendHandlerMap = {}
        self.publisherHandlerMap = {}

    def setHandlerForBackend(self, backend, handler):
        if backend in self.backendHandlerMap:
            raise RegistryError(" Backend already registered with another Handler. Configuration Error!")
        else:
            self.backendHandlerMap[backend] = handler

        
    def getHandlerForBackend(self, backend):
        if backend in self.backendHandlerMap:
            return self.backendHandlerMap[backend]
        else:
            raise RegistryError("No Handler registered with Backend. Did you register it?")

    def getPublisher(self, publisher):
        if publisher in self.publisherHandlerMap:
            return self.publisherHandlerMap[publisher]
        else:
            raise RegistryError(f"No Handler registered with Publisher {publisher}. Did you register it?")


    def setPublisher(self, publisher, handler):
        if publisher in self.backendHandlerMap:
            raise RegistryError(" Publisher already registered with another Handler. Configuration Error!")
        else:
            self.publisherHandlerMap[publisher] = handler



GLOBAL_SETTINGS_REGISTRY = SettingRegistry()

def get_settings_registry()-> SettingRegistry:
    return GLOBAL_SETTINGS_REGISTRY
