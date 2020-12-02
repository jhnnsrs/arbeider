from delt.handlers.base import BaseHandlerSettings
import logging

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer
from django.conf import settings

from balder.mutations import assignations
from delt.consumers.utils import (AssignationMessageSerializer, deserialized,
                                  send_assignation_to_channel, send_assignation_to_gateway, 
                                  send_provision_to_gateway)
from delt.constants.lifecycle import PROVISION_DENIED_CREATION, PROVISION_SUCCESS_CREATED
from delt.models import Assignation, Node, Pod, Provision
from delt.serializers import (PodSerializer, ProvisionMessageSerializer,
                              ProvisionSerializer)

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()


class ProvisionConsumerException(Exception):
    pass


class ProvisionConsumer(SyncConsumer):
    settings = None

    def __init__(self) -> None:
        if self.settings is None or not isinstance(self.settings, BaseHandlerSettings):
            logger.error(f"Provision Consumer of Class {self.__class__.__name__} does not have a valid settings handler!")
            raise ProvisionConsumerException("You must provide a valid BaseHandlerSettings class to your Provision Consumer")
        super().__init__()


    @deserialized(ProvisionMessageSerializer)
    def on_provision_pod(self, message):
        provision = message["provision"]
        logger.info(f"Trying to provision {provision}")
        try:
            pod = self.get_pod(provision)
            assert pod is not None, "We received no Pod from provisioner, Provisioners should either return Pod or error. Please Implement logic Correctly"
            success_provision = Provision.objects.get(reference=provision.reference)
            success_provision.pod = pod
            success_provision.status = PROVISION_SUCCESS_CREATED
            success_provision.save()

            logger.info(f"We have provisioned a Pod, waiting for it to become ready {provision.pod}")
            send_provision_to_gateway(success_provision, "provision_success")
        except Exception as e:
            logger.error(f"Error on Provision {provision}, {str(e)}")
            failed_provision = Provision.objects.get(reference=provision.reference)
            failed_provision.status = PROVISION_DENIED_CREATION + f"Error on Provision {provision}, {str(e)}"
            failed_provision.save()
            
            send_provision_to_gateway(failed_provision, "provision_error")

    def get_pod(self, provision: Provision):
        raise NotImplementedError("Please derived a get_pod class in your consumer")

    def assign_inputs(self, assignation: Assignation):
        raise NotImplementedError("Please derived a assign_inputs class in your consumer")


    @deserialized(AssignationMessageSerializer)
    def on_assign_job(self, message):
        assignation = message["assignation"]
        try:
            job = self.assign_inputs(assignation)
            send_assignation_to_gateway(assignation, "assignation_success")
        except Exception as e:
            send_assignation_to_gateway(assignation, "assignation_failed")


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
