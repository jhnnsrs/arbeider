
import logging

from django.forms.models import model_to_dict

import unflatten
from delt import publishers
from delt.bouncers.context import BouncerContext
from delt.bouncers.job.base import BaseJobBouncer
from delt.bouncers.node.base import BaseNodeBouncer
from delt.bouncers.pod.base import BasePodBouncer
from delt.consumers.utils import send_provision_to_gateway
from delt.constants.lifecycle import *
from delt.models import Assignation, Job, Node, Pod, Provision
from delt.orchestrator import get_orchestrator
from delt.publishers.base import BasePublisher
from delt.publishers.utils import publish_to_event
from delt.selector import get_provider_for_selector
from delt.utils import pipe

logger = logging.getLogger(__name__)




def publishToPodEvents(pod: Pod):

    pod = pod
    status = pod.status

    # Some Pods can be active by default (persistent Pods like Channelworkers, for example), these will get invoked
    if status == POD_ACTIVE:
        publish_to_event("pod_ready", pod)
    if status == POD_PENDING:
        publish_to_event("pod_pending", pod)
    if status == POD_FAILURE:
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
    
def assignation_succeeded_pipe(assignation):
    # A Successfull provision will results in a Pod that is either Active or Pending by default
    # Therefore we can always publish it
    publish_to_event("assignation_succeeded",assignation)


def assignation_done_pipe(assignation):
    # A Successfull provision will results in a Pod that is either Active or Pending by default
    # Therefore we can always publish it
    publish_to_event("assignation_done",assignation)


def assignation_progress_pipe(assignation):
    publish_to_event("assignation_progress", assignation)

def assignation_failed_pipe(assignation):
    # A Successfull provision will results in a Pod that is either Active or Pending by default
    # Therefore we can always publish it
    publish_to_event("assignation_failed",assignation)


def unprovision_failed_pipe(provision):
    logger.error("Provision failed")

def unprovision_succeeded_pipe(provision):
    logger.info("Provision succeeded")

# Pod Lifecycle Pipes

def pod_initializing_pipe(pod: Pod):
    publish_to_event("pod_initializing",pod)


def pod_initialized_pipe(pod: Pod):
    publish_to_event("pod_initialized",pod)

def pod_activated_pipe(pod: Pod):
    publish_to_event("pod_activated",pod)



# Provision Pod

# We need this ugly ping pong because of how Graphene and Django Channels handle subscriptions.
# Possibly a new mechanism for confirmation is a good idea.


#ping
@pipe("republish_provision")
def republish_provision_pipe(provision: Provision):
    send_provision_to_gateway(provision, "republish_provision")

#pong
@pipe("republished_provision")
def republished_provision_pipe(provision: Provision):
    publish_to_event("republished_provision", provision)


@pipe("provision_pod")
def provision_pod_pipe(context: BouncerContext, reference, node: Node, selector: str, parent):
    ''' Make sure the reference here is unique'''
    
    #Check if a Provsion already exists under this reference
    try:
        provision = Provision.objects.get(reference=reference)
        if provision.node != node:
            raise Exception("This provision already exists is another configuration. Cannot re-assign! Please use different reference (UUID)")
    except Provision.DoesNotExist as e:
        orchestrator = get_orchestrator()

        # We check for the Permissions to provision Pods on this NodePod
        bouncer: BaseNodeBouncer = orchestrator.getBouncerForNodeAndContext(node, context)
        bouncer.can_provision_pods()

        #Check were we will Provide
        provider, subselector = get_provider_for_selector(selector)
        
        # Check permissions of user to provide on this Node and this Provider
        bouncer.can_provide_on(provider)

        user = bouncer.user


        # If we reached here without exceptions our Pod is able to be Provisioned
        provision = Provision.objects.create(
            reference=reference,
            node=node,
            provider=provider,
            subselector= subselector,
            status= PROVISION_PENDING,
            user=user,
            parent=parent,
            token= context.token,
            active=True
        )

        
        
        handler = orchestrator.getHandlerForProvider(provider)
        logger.info(f"Send to Provisioner {handler.__class__.__name__}")
        handler.on_new_provision(provision)

    # Pods are assigned to a Node and a creating User, the provision substring helps identifying the right entitiy
    
    return provision

#@pipe("assign_inputs")
def assign_inputs_pipe(context: BouncerContext, reference, pod: Pod, inputs: dict):
    inputs = unflatten.unflatten(inputs)

    #Check if a Provsion already exists under this reference
    try:
        assignation = Assignation.objects.get(reference=reference)
        if assignation.pod != pod:
            raise Exception("This Job already exists is another configuration. Cannot re-assign! Please use different reference (UUID)")
    except Assignation.DoesNotExist as e:

        orchestrator = get_orchestrator()

        # We check for the Permissions to assign to this Pod
        bouncer: BasePodBouncer = orchestrator.getBouncerForPodAndContext(pod, context)
        bouncer.can_assign_job()

        #We get the user from the bouncer
        user = bouncer.user

        # We are validating the inputs according to the Node Specifications
        validator = orchestrator.getValidatorForNode(pod.node)
        validator.validateInputs(inputs)

        # We assign the Job to the Handler

        
        logger.info(f"Will Assign a New Job with reference {reference}")
        assignation = Assignation.objects.create(
            reference=reference,
            pod=pod,
            creator=user,
            inputs=inputs,
            status="pending",
            token= context.token
        )

        # Jobs are assigned to a Pod with the Inputs and linked to a User, and a unique Reference
        orchestrator.getHandlerForPod(pod).on_assign_job(assignation)

    return assignation
