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
                              PodSerializer, ProvisionMessageSerializer,
                              ProvisionSerializer)

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

    @deserialized(ProvisionMessageSerializer)
    def provision_success(self, message):
        provision = message["provision"]
        logger.info(f"Provision Succeed {provision}")
        provision_succeeded_pipe(provision)

    @deserialized(ProvisionMessageSerializer)
    def provision_failed(self, message):
        provision = message["provision"]
        logger.error(f"Provision Failed {provision}")
        provision_failed_pipe(provision)
    
    def pod_updated(self, message: dict):
        data = message["data"]
        pod = Pod.objects.get(id=data["id"])
        pod_updated_pipe(pod)
    def pod_provisioned(self, message: dict):
        data = message["data"]
        pod = Pod.objects.get(id=data["id"])
        pod_provisioned_pipe(pod)

    def pod_updated(self, message: dict):
        data = message["data"]
        pod = Pod.objects.get(id=data["id"])
        pod_updated_pipe(pod)
