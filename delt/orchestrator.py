import logging

from delt.bouncers.base import BaseBouncer
from delt.bouncers.context import BouncerContext
from delt.bouncers.job.base import BaseJobBouncer
from delt.bouncers.node.base import BaseNodeBouncer
from delt.bouncers.pod.base import BasePodBouncer
from delt.handlers.base import BaseHandler
from delt.models import Job, Node, Pod
from delt.validators.base import BaseValidator

logger = logging.getLogger(__name__)

class OrchestratorError(Exception):
    pass

class Orchestrator():

    def __init__(self):
        #TODO Set this lazyliy from the Settings
        self.providerHandlerMap = {}
        self.publisherHandlerMap = {}
        self.defaultJobBouncer = None
        self.defaultPodBouncer = None
        self.defaultNodeBouncer = None
        self.identifierValidatorMap = {}

    def setDefaultJobBouncer(self, bouncer):
        assert issubclass(bouncer, BaseJobBouncer), "You must provide a Valid JobBouncer class"
        self.defaultJobBouncer = bouncer

    def setDefaultPodBouncer(self, bouncer):
        assert issubclass(bouncer, BasePodBouncer), "You must provide a Valid PodBouncer class"
        self.defaultPodBouncer = bouncer

    def setDefaultNodeBouncer(self, bouncer):
        assert issubclass(bouncer, BaseNodeBouncer), "You must provide a Valid NodeBouncer class"
        self.defaultNodeBouncer = bouncer

    def getBouncerForPodAndContext(self, pod: Pod, context: BouncerContext):
        return self.defaultPodBouncer(pod, context)

    def getBouncerForNodeAndContext(self, node: Node, context: BouncerContext):
        return self.defaultNodeBouncer(node, context)

    def getBouncerForJob(self, job: Job):
        return self.defaultJobBouncer


    def setValidatorForNodeIdentifier(self, identifier, validator: BaseValidator):
        assert issubclass(type(validator), BaseValidator), "You must provide a valid Validator that derives from Base Validator"
        logger.info(f"Registering Validator at {identifier}")
        self.identifierValidatorMap[identifier] = validator

    def getValidatorForNodeIdentifier(self, identifier):
        assert identifier in self.identifierValidatorMap, "There is no Validator registered for this Node"
        return self.identifierValidatorMap[identifier]

    def getValidatorForNode(self, node: Node):
        return self.getValidatorForNodeIdentifier(node.identifier)


    def setHandlerForProvider(self, provider, handler):
        if provider in self.providerHandlerMap:
            pass
            #raise RegistryError(" Backend already registered with another Handler. Configuration Error!")
        else:
            self.providerHandlerMap[provider] = handler
 
    def getHandlerForProvider(self, provider)-> BaseHandler:
        if provider in self.providerHandlerMap:
            return self.providerHandlerMap[provider]
        else:
            raise OrchestratorError(f"No Handler registered with Provider {provider}. Did you register it?")

    def getHandlerForPod(self, pod: Pod) -> BaseHandler:
        return self.getHandlerForProvider(pod.provider)

    def getPublishersForEvent(self, event):
        publishers = []
        for provider, publisher in self.publisherHandlerMap.items():
            if event in publisher.settings.fields:
                publishers.append(publisher)
        return publishers

    def getPublisher(self, publisher):
        if publisher in self.publisherHandlerMap:
            return self.publisherHandlerMap[publisher]
        else:
            raise OrchestratorError(f"No Handler registered with Publisher {publisher}. Did you register it?")


    def setPublisher(self, publisher, handler):
        if publisher in self.publisherHandlerMap:
            pass
            #raise RegistryError(" Publisher already registered with another Handler. Configuration Error!")
        else:
            self.publisherHandlerMap[publisher] = handler



orchestrator = None

def get_orchestrator()-> Orchestrator:
    global orchestrator
    if orchestrator is None:
        orchestrator = Orchestrator()
    return orchestrator
