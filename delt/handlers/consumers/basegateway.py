from delt.handlers.consumers.base import BaseConsumer
from delt.consumers.utils import deserialized
import logging

from delt.models import Assignation, Provision
from delt.serializers import  AssignationMessageSerializer, ProvisionMessageSerializer
from delt.pipes import assignation_critical_pipe, assignation_succeeded_pipe, provision_failed_pipe, provision_succeeded_pipe

logger = logging.getLogger(__name__)


class BaseGatewayConsumer(BaseConsumer):
    
    @deserialized(ProvisionMessageSerializer, colapse="provision")
    def provision_succeeded(self, prov: Provision):
        provision_succeeded_pipe(prov)

    @deserialized(ProvisionMessageSerializer, colapse="provision")
    def provision_failed(self, prov: Provision):
        provision_failed_pipe(prov)

    @deserialized(AssignationMessageSerializer, colapse="assignation")
    def assignation_succeeded(self, assignation: Assignation):
        assignation_succeeded_pipe(assignation)


    @deserialized(AssignationMessageSerializer, colapse="assignation")
    def assignation_criticaled(self, assignation: Assignation):
        assignation_critical_pipe(assignation)