from balder.notifier.registry import get_notifying_registry
from balder.subscriptions.base import BaseSubscription


def initialPayload(payloadConstructor):

    def classDecorator(theclass):
        assert issubclass(theclass, BaseSubscription), "Class needs to Subclass Base Subscription"
        theclass.initialPayloadHook = payloadConstructor
        if theclass.subscriptionUUID is None:
            theclass.subscriptionUUID = theclass.__name__


        get_notifying_registry().setSubscriptionForUUID(theclass.subscriptionUUID, theclass)

        return theclass

    return classDecorator
