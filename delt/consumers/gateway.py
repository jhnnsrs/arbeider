import logging

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer

from balder.utils import serializerToDict
from delt.consumers.utils import deserialized
from delt.models import Job, Pod
from delt.pipes import (assignation_done_pipe, assignation_failed_pipe, assignation_progress_pipe, assignation_succeeded_pipe,
                        job_assigned_pipe, pod_provisioned_pipe,
                        pod_updated_pipe, provision_failed_pipe,
                        provision_succeeded_pipe, republished_provision_pipe,
                        unprovision_failed_pipe, unprovision_succeeded_pipe)
from delt.serializers import (AssignationMessageSerializer,
                              AssignationSerializer, JobSerializer,
                              PodSerializer, ProvisionMessageSerializer,
                              ProvisionSerializer)

logger = logging.getLogger(__name__)


channel_layer = get_channel_layer()

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

    @deserialized(AssignationMessageSerializer)
    def assignation_success(self, message):
        assignation = message["assignation"]
        logger.info(f"Assignation Succeed {assignation}")
        assignation_succeeded_pipe(assignation)


    @deserialized(AssignationMessageSerializer)
    def assignation_done(self, message):
        assignation = message["assignation"]
        logger.info(f"Assignation Succeed {assignation}")
        assignation_done_pipe(assignation)

    @deserialized(AssignationMessageSerializer)
    def assignation_progress(self, message):
        assignation = message["assignation"]
        logger.info(f"Assignation Progress {assignation}")
        assignation_progress_pipe(assignation)


    @deserialized(AssignationMessageSerializer)
    def assignation_failed(self, message):
        assignation = message["assignation"]
        logger.info(f"Provision Succeed {assignation}")
        assignation_failed_pipe(assignation)

    @deserialized(ProvisionMessageSerializer)
    def provision_error(self, message):
        provision = message["provision"]
        logger.error(f"Provision error received {provision}")
        provision_failed_pipe(provision)

    # ping of Provision for provide initial payload
    @deserialized(ProvisionMessageSerializer)
    def republish_provision(self, message):
        provision = message["provision"]
        logger.error(f"Provision Republish {provision}")
        #pong of provision
        async_to_sync(channel_layer.send)("assignation-13",{"type": "on_init_acknowledged", "data" : {}})
        print("OISNOEINFOISNEFOINSOEIFNOSIENFOPSIENF")
        republished_provision_pipe(provision)
    
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
