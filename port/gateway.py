import logging

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer
from django.conf import settings

from delt.bouncers.context import BouncerContext
from delt.consumers.utils import deserialized, send_provision_to_gateway
from delt.context import Context
from delt.models import Node, Pod, Provision
from delt.pipes import (pod_activated_pipe, pod_initialized_pipe,
                        provision_pod_pipe)
from delt.pod import PODACTIVE, PODINIT
from port.models import Flowly
from port.serializers import (ActivationRequestSerializer,
                              InitRequestSerializer,
                              ProvisionRequestSerializer)
from port.utils import provision_channel_from_id, assignation_channel_from_id

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()

logger.warn("HAOINSOIENOIENOIENOAINOEINOAIENs")

class PortGateway(SyncConsumer):


    def __init__(self, scope):
        logger.info("WE HAVE GOOTEN HERE YOU MONSTER")
        super().__init__(scope)

    @deserialized(ProvisionRequestSerializer)
    def on_provision_request(self, message):
        parent = message["parent"]
        logger.info(f"Trying to provision pod for parent provision {parent}")
        try:
            node = message["node"]
            selector = message["selector"]
            token = message["token"]
            reference = message["reference"]
            context = BouncerContext(token=token)
            provision = provision_pod_pipe(context, reference, node, selector, parent)
            logger.info(f"We have request to Provision a Pod, waiting for it to become procesed py provider {provision.provider}")
        except Exception as e:
            logger.error(f"Error on Provision {provision}, {str(e)}")
            self.provision_request_failed(e)


    @deserialized(InitRequestSerializer)
    def on_init_request(self, message):
        pod = message["pod"]
        try:
            logger.info(f"Acknowledging initialization of Pod {pod}")
            pod.status = PODINIT
            pod.save()
            pod_initialized_pipe(pod)
            
            # The backend has acknowledged the init request and the pod may start activation

            # We will send the initial provision request from every ACTIVE provision to this container
            #TODO: Implement who is active??
            provision_channel = provision_channel_from_id(pod.id)
            logger.info(f"provision_channel: {provision_channel}")
            async_to_sync(channel_layer.send)(provision_channel,{"type": "on_init_acknowledged", "data" : {}})
        except Exception as e:
            logger.error(f"Error on Initializing {pod}, {str(e)}")

    @deserialized(ActivationRequestSerializer)
    def on_activate_pod(self, message):
        pod = message["pod"]
        try:
            logger.info(f"Acknowledging Activation of Pod {pod}")
            pod.status = PODACTIVE
            pod.save()
            logger.info(f"Acknowledging activation of Pod {pod}")
            pod_activated_pipe(pod)
        except Exception as e:
            raise e

    def provision_request_failed(self, e):
        logger.error(f"We have failed to Provision a Pod {e} ")
