import graphene


class Registry():

    def __init__(self):
        self.fieldQueryMap = {}
        self.fieldSubscriptionMap = {}
        self.fieldMutationMap = {}
        self.subscriptionMap = {}

    def getQueryFields(self):
        return self.fieldQueryMap
    
    def setSubscription(self, field, value):
        self.subscriptionMap[field] = value

    def getSubscription(self, field):
        return self.subscriptionMap[field]

    def setQueryField(self, field, value):
        self.fieldQueryMap[field] = value

    def getSubscriptionFields(self):
        return self.fieldSubscriptionMap
    
    def setSubscriptionField(self, field, value):
        self.fieldSubscriptionMap[field] = value

    def getMutationFields(self):
        return self.fieldMutationMap
    
    def setMutationField(self, field, value):
        self.fieldMutationMap[field] = value


registry = None

def get_registry()-> Registry:
    global registry
    if registry is None:
        registry = Registry()
    return registry
