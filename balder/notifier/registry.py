import logging


logger = logging.getLogger()



class NotifyingRegistry():

    def __init__(self):
        self.subscriptionUUIDMap = {}

    
    def setSubscriptionForUUID(self, uuid, subscription):
        logger.error(f"Making this in {uuid}")
        self.subscriptionUUIDMap[uuid] = subscription

    def getSubscriptionForUUID(self, uuid):
        if uuid in self.subscriptionUUIDMap:
            return self.subscriptionUUIDMap[uuid]
        else:
            raise Exception(f"Did Not find Subscription for UUID {uuid}. Massive Configuration Error")


notifiyingregistry = None

def get_notifying_registry()-> NotifyingRegistry:
    global notifiyingregistry
    if notifiyingregistry is None:
        notifiyingregistry = NotifyingRegistry()
    return notifiyingregistry