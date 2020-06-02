
import logging

from delt import publishers
from delt.bouncers.context import BouncerContext
from delt.bouncers.job.base import BaseJobBouncer
from delt.bouncers.node.base import BaseNodeBouncer
from delt.bouncers.pod.base import BasePodBouncer
from delt.context import Context
from delt.models import Job, Node, Pod
from delt.orchestrator import get_orchestrator
from delt.pod import PODFAILED, PODPENDING, PODREADY
from delt.publishers.base import BasePublisher
from delt.publishers.utils import publish_to_event
from delt.selector import get_handler_for_selector, get_provider_for_selector
from delt.settingsregistry import get_settings_registry

logger = logging.getLogger(__name__)


def publishToPodEvents(pod: Pod):

    pod = pod
    status = pod.status

    # Some Pods can be active by default (persistent Pods like Channelworkers, for example), these will get invoked
    if status == PODREADY:
        publish_to_event("pod_ready", pod)
    if status == PODPENDING:
        publish_to_event("pod_pending", pod)
    if status == PODFAILED:
        publish_to_event("pod_failed", pod)


#Publisher Pipes
def pod_provisioned_pipe(pod: Pod):
    publish_to_event("pod_provisioned",pod)

def pod_updated_pipe(pod: Pod):
    logger.info("Updating Pod")
    publishToPodEvents(pod)

def job_assigned_pipe(job: Job):
    logger.info("Updating Pod")
    publish_to_event("job_assigned",job)

# Handler Results

def provision_failed_pipe(provision):
    logger.error(f"{provision}")
    publish_to_event("provision_failed",provision)

def provision_succeeded_pipe(provision):
    
    # A Successfull provision will results in a Pod that is either Active or Pending by default
    # Therefore we can always publish it
    publish_to_event("provision_succeeded",provision)
    publishToPodEvents(provision["pod"])
    


def unprovision_failed_pipe(provision):
    logger.error("Provision failed")

def unprovision_succeeded_pipe(provision):
    logger.info("Provision succeeded")

# INCOMING PIPES



def provision_pod_pipe(reference, node: Node, selector: str, context: BouncerContext):

    orchestrator = get_orchestrator()

    # We check for the Permissions to provision Pods on this NodePod
    bouncer: BaseNodeBouncer = orchestrator.getBouncerForNodeAndContext(node, context)
    bouncer.can_provision_pods()

    #Check were we will Provide
    provider, subselector = get_provider_for_selector(selector)
    
    # Check permissions of user to provide on this Node and this Provider
    bouncer.can_provide_on(provider)

    user = bouncer.user
    # Send to Provisioner
    handler = orchestrator.getHandlerForProvider(provider)

    # Pods are assigned to a Node and a creating User, the provision substring helps identifying the right entitiy
    handler.on_provide_pod(reference, node, subselector, user)
    logger.info("Send to Provisioner")


def assign_job_pipe(reference, pod: Pod, inputs: dict, context: BouncerContext):

    orchestrator = get_orchestrator()

    # We check for the Permissions to assign to this Pod
    bouncer: BasePodBouncer = orchestrator.getBouncerForPodAndContext(pod, context)
    bouncer.can_assign_job()

    #We get the user from the bouncer
    user = bouncer.user

    # We are validating the inputs according to the Node Specifications
    validator = orchestrator.getValidatorForNode(pod.node)
    validator.validateInputs(inputs)

    # We assign the Pod to the Handler
    
    # Jobs are assigned to a Pod with the Inputs and linked to a User, and a unique Reference
    orchestrator.getHandlerForPod(pod).on_assign_job(reference, pod, inputs, user)
