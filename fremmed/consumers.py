import logging
import re
import uuid

from guardian.shortcuts import assign_perm
from delt.constants.lifecycle import POD_ACTIVE
from balder.utils import serializerToDict
from delt import selector as selectors
from delt.consumers.job import JobConsumer
from delt.consumers.utils import deserialized
from delt.consumers.provisioner import ProvisionConsumer
from delt.models import Job
from extensions.fremmed.subscriptions import GateSubscription
from fremmed.models import FrontendPod
from fremmed.serializers import ActivationSerializer

logger = logging.getLogger(__name__)


class FremmedProvisionConsumer(ProvisionConsumer):
    provider = "fremmed"

    def get_pod(self, provision):
        logger.info(f"Received {provision}")

        if selectors.unique(provision["subselector"]):
            pod, _ = FrontendPod.objects.get_or_create(node=provision["node"], persistent=False, provider="fremmed", reference=provision["reference"])
            logger.info("Creating Frontend pod with user Permissions")
            assign_perm('access_pod', provision["user"], pod)

        if selectors.all(provision["subselector"]):
            pod, _ = FrontendPod.objects.get_or_create(node=provision["node"], persistent=False, provider="fremmed", reference=provision["reference"])
            logger.info("Creating Frontend pod with user Permissions")
            assign_perm('access_pod', provision["user"], pod)

        return pod

    @deserialized(ActivationSerializer)
    def activate_pod(self, data):
        pod = data["pod"]
        
        if pod.frontendpod is None: raise NotImplementedError("You provided the wrong Pod here, this is a unique one")
        
        pod.status = POD_ACTIVE
        pod.save()
        for provision in pod.provisions.all():
            self.on_provision_update(provision)

        
        logger.info("Pod Updated")




class FremmedJobConsumer(JobConsumer):

    def assign_job(self, reference, pod, inputs, user):
        logger.info(f"Received Job {reference} for pod {pod}")

        pod = pod

        if pod.frontendpod is None: 
            raise("Not the right job for the task")
        else:
            gate = pod.unique
            node = pod.node

        pod.status = "Parsing"
        pod.save()
        self.pod_updated(pod)

        job = Job.objects.create(reference=reference, pod=pod, inputs=inputs, creator=user)
        serialized = self.job_assigned(job)
