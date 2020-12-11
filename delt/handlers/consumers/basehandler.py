from rest_framework.exceptions import ValidationError
from delt.handlers.exceptions import HandlerException, SelectorMalformedException
from delt.enums import AssignationStatus, PodStatus, ProvisionStatus
from delt.handlers.consumers.base import BaseConsumer
from delt.handlers.protocol import Protocol
from delt.consumers.utils import deserialized
import logging

from delt.selectors.base import BaseSelector
from delt.models import Assignation, Provision
from delt.serializers import  AssignationMessageSerializer, ProvisionMessageSerializer

logger = logging.getLogger(__name__)

class BaseHandlerConsumer(BaseConsumer):
    selectorClass = None

    def __init__(self) -> None:
        super().__init__()

    @deserialized(ProvisionMessageSerializer, colapse="provision")
    def provision_in(self, prov: Provision):
        try:
            try:
                selectodict = self.handler.env.getSelectorFromKwargs(prov.kwargs)
            except ValidationError as e:
                raise SelectorMalformedException(e)


            pod = self.handler.provide(prov.node, selectodict)
            pod.active = True
            pod.status = PodStatus.ACTIVE
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
        
