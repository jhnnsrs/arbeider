from delt.handlers.exceptions import HandlerException
from delt.enums import AssignationStatus, ProvisionStatus
from delt.handlers.consumers.base import BaseConsumer
from delt.handlers.protocol import Protocol
from delt.consumers.utils import deserialized
import logging

from delt.selector import Selector
from delt.models import Assignation, Provision
from delt.serializers import  AssignationMessageSerializer, ProvisionMessageSerializer

logger = logging.getLogger(__name__)

class BaseHandlerConsumer(BaseConsumer):

    @deserialized(ProvisionMessageSerializer, colapse="provision")
    def provision_in(self, prov: Provision):
        try:
            pod = self.handler.provide(prov.node, Selector(prov.subselector))
            pod.active = True
            pod.save()

            # Updating Provision With Pod
            prov.pod = pod
            prov.status = ProvisionStatus.ASSIGNED
            prov.statusmessage = f"Wonderful assigned through {self.handler.env.getProviderName()}"
            prov.save()

            self.provision_to_gateway(Protocol.PROVISION_SUCCEEDED, prov)
        except HandlerException as e:
            prov.status = ProvisionStatus.CRITICAL
            prov.statusmessage = str(e)
            prov.save()
            self.provision_to_gateway(Protocol.PROVISION_FAILED, prov)

    def provision_to_gateway(self, protocol, provision: Provision):
        self.gateway.contact(protocol, {"provision": provision}, serializer= ProvisionMessageSerializer)
        

    def assignation_to_gatway(self, protocol: str, assignation: Assignation):
         self.gateway.contact(protocol, {"assignation": assignation}, serializer= AssignationMessageSerializer)


    @deserialized(AssignationMessageSerializer, colapse="assignation")
    def assignation_in(self, assignation: Assignation):
        try:
            assigned = self.handler.assign(assignation)
            if assigned:
                assignation.status = AssignationStatus.ASSIGNED
                assignation.save()
                self.assignation_to_gatway(Protocol.ASSIGNATION_SUCCEEDED, assignation)
            else:
                assignation.status = AssignationStatus.DENIED
                assignation.save()
                self.assignation_to_gatway(Protocol.ASSIGNATION_DENIED, assignation)

        except Exception as e:
            assignation.status = str(e)
            assignation.save()
            self.assignation_to_gatway(Protocol.ASSIGNATION_CRITICALED, assignation)
        
