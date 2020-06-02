import logging
import re
import uuid

from guardian.shortcuts import assign_perm

from balder.subscriptions.provision import ProvisionSubscription
from balder.utils import serializerToDict
from delt import selector as selectors
from delt.consumers.exceptions import NoMatchablePod
from delt.consumers.job import JobConsumer
from delt.consumers.provisioner import ProvisionConsumer
from delt.consumers.utils import deserialized
from delt.models import Job, Provision
from delt.pod import PODPENDING
from delt.serializers import JobSerializer, PodSerializer
from delt.settingsregistry import get_settings_registry
from extensions.fremmed.subscriptions import GateSubscription
from port.models import Flowly

logger = logging.getLogger(__name__)


class PortProvision(ProvisionConsumer):
    provider = "port"

    def get_pod(self, provision):
        logger.info(f"Received {provision}")

        # Are we provisioning a Flow???
        flow = provision["node"].flownode
        if flow is None: raise NotImplementedError("We are still only able to provision FLOWS")

        pod = Flowly.objects.create(
            node = flow,
            podclass = "flow-pod",
            status = PODPENDING,
            provider = self.provider,
            persistent = False
        )


        return pod
