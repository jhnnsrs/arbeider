import logging

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer

from delt.consumers.utils import (deserialized, send_provision_to_gateway,
                                  send_unprovision_to_gateway)
from delt.context import Context
from delt.models import Node, Pod, Provision
from delt.pod import PODACTIVE
from delt.serializers import PodSerializer, ProvisionSerializer

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()


class ProvisionConsumer(SyncConsumer):

    @deserialized(ProvisionSerializer)
    def on_provision_pod(self, provision):
        logger.info(f"Trying to provision {provision}")
        try:
            pod = self.get_pod(provision)
            assert pod is not None, "We received a no Pod from provisioner, Provisioners should either return Pod or error. Please Implement logic Correctly"
            provision_model = Provision.objects.create(**{**provision, "pod": pod}) #TODO: Do we need any reference to this?
            self.on_provision_success(provision, pod)
        except Exception as e:
            logger.error(f"Error on Provision {provision}, {str(e)}")
            self.on_provision_error(provision, str(e))

    def provision_pod(self, reference, node: Node, subselector: str, user):
        raise NotImplementedError("Please derived a provision_pod class in your consumer")

    def on_provision_error(self, provision, error):
        provision = {**provision, "error": error}
        self.on_provision_update(provision)

    def on_provision_update(self, provision):
        logger.info(f"Provision Updated {provision}")
        send_provision_to_gateway(provision)

    def on_provision_success(self, provision, pod):
        logger.info(f"We have provisioned a Pod, waiting for it to become ready {pod}")
        provision = {**provision, "pod": pod}
        self.on_provision_update(provision)



    def on_pod_update(self, pod):
        send_pod_to_gateway(pod)

    def on_pod_failure(self, pod):
        logger.error(f"Pod {pod} has failed")

    def on_pod_pending(self, pod):
        logger.info(f"Pod {pod} is passive or pending and not eligible for Assignation")

    def on_pod_ready(self, pod):
        logger.info(f"Pod {pod} is now ready for Jobs")

    def on_pod_pending(self, pod):
        logger.info(f"Pod {pod} is now restarting")

    def on_unprovision_pod(self, unprovision):
        try:
            self.unprovision_pod(unprovision)
        except Exception as e:
            self.on_unprovision_error(self, unprovision, str(e))

    def on_unprovision_error(self, provision, error):
        provision = {**provision, "error": error}
        send_unprovision_to_gateway(provision)

    def on_unprovision_success(self, provision, pod):
        logger.info("We have unprovision a Pod, waiting for it to become ready")
        provision = {**provision, "error": None}
        send_unprovision_to_gateway(provision)
