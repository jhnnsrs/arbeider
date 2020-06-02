import logging
import re
import uuid

from guardian.shortcuts import assign_perm
from delt.pod import PODREADY
from balder.subscriptions.provision import ProvisionSubscription
from balder.utils import serializerToDict
from delt import selector as selectors
from delt.consumers.job import JobConsumer
from delt.consumers.utils import deserialized
from delt.consumers.provisioner import ProvisionConsumer
from delt.models import Job, Provision
from delt.serializers import JobSerializer, PodSerializer
from delt.settingsregistry import get_settings_registry
from extensions.fremmed.subscriptions import GateSubscription
from fremmed.models import FrontendPod
from fremmed.serializers import ActivationSerializer

logger = logging.getLogger(__name__)


class FremmedProvisionConsumer(ProvisionConsumer):
    provider = "fremmed"

    def get_pod(self, provision):
        print(provision)
        logger.info(f"Received {provision}")

        if selectors.unique(provision["subselector"]):
            pod, _ = FrontendPod.objects.get_or_create(node=provision["node"], persistent=False, provider="fremmed", reference=provision["reference"])
            logger.info("Creating Frontend pod with user Permissions")
            assign_perm('access_pod', provision["user"], pod)

        return pod

    @deserialized(ActivationSerializer)
    def activate_pod(self, data):
        pod = data["pod"]
        
        if pod.frontendpod is None: raise NotImplementedError("You provided the wrong Pod here, this is a unique one")
        
        pod.status = PODREADY
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
