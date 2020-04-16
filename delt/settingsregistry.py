
class RegistryError(Exception):
    pass


class SettingRegistry():

    def __init__(self):
        #TODO Set this lazyliy from the Settings
        self.backendHandlerMap = {}

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

    def getPublishers(self, backend):
        raise NotImplementedError("Not Implement yet")



GLOBAL_SETTINGS_REGISTRY = SettingRegistry()

def get_settings_registry():
    return GLOBAL_SETTINGS_REGISTRY
