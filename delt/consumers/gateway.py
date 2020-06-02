import logging

from channels.consumer import SyncConsumer

from balder.utils import serializerToDict
from delt.consumers.utils import deserialized
from delt.models import Job, Pod
from delt.pipes import (job_assigned_pipe, pod_provisioned_pipe,
                        pod_updated_pipe, provision_failed_pipe,
                        provision_succeeded_pipe, unprovision_failed_pipe,
                        unprovision_succeeded_pipe)
from delt.serializers import (AssignationSerializer, JobSerializer,
                              PodSerializer, ProvisionSerializer)

logger = logging.getLogger(__name__)

class GatewayConsumer(SyncConsumer):

    def job_assigned(self, message: dict):
        data = message["data"]
        job = Job.objects.get(id=data["id"])
        job_assigned_pipe(job)

    def job_updated(self, message: dict):
        data = message["data"]
        serialized = JobSerializer(data=data)
        job_dict = serializerToDict(serialized)

        logger.info(f"Updated Job {job_dict}")

    
    @deserialized(ProvisionSerializer)
    def provision_updated(self, provision):
        if "error" in provision and provision["error"] is not None:
            logger.error("Provision Failed")
            provision_failed_pipe(provision)
        if "pod" in provision and provision["pod"] is not None:
            logger.info("Provision Succeed")
            provision_succeeded_pipe(provision)


    def pod_updated(self, message: dict):
        data = message["data"]
        pod = Pod.objects.get(id=data["id"])
        pod_updated_pipe(pod)


    @deserialized(ProvisionSerializer)
    def unprovision_success(self, provision):
        unprovision_succeeded_pipe(provision)
        logger.info("Unprovisin Succeeded")

    @deserialized(ProvisionSerializer)
    def unprovision_error(self, provision):
        unprovision_failed_pipe(provision)
        logger.info("Unprovision Failed")

    def pod_provisioned(self, message: dict):
        data = message["data"]
        pod = Pod.objects.get(id=data["id"])
        pod_provisioned_pipe(pod)

    def pod_updated(self, message: dict):
        data = message["data"]
        pod = Pod.objects.get(id=data["id"])
        pod_updated_pipe(pod)
