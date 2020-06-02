import logging
import re
import uuid

from guardian.shortcuts import assign_perm

from balder.subscriptions.provision import ProvisionSubscription
from balder.utils import serializerToDict
from delt import selector as selectors
from delt.consumers.job import JobConsumer
from delt.consumers.utils import deserialized
from delt.consumers.provisioner import ProvisionConsumer
from delt.consumers.exceptions import NoMatchablePod
from delt.models import Job, Provision
from delt.serializers import JobSerializer, PodSerializer
from delt.settingsregistry import get_settings_registry
from extensions.fremmed.subscriptions import GateSubscription
from kanal.models import KanalPod

logger = logging.getLogger(__name__)


class KanalProvisionConsumer(ProvisionConsumer):
    provider = "kanal"

    def get_pod(self, provision):
        logger.info(f"Received {provision}")

        node = provision["node"]

        if selectors.all(provision["subselector"]):
            pod = KanalPod.objects.filter(node=provision["node"]).first()
            if not pod:
                raise NoMatchablePod(f"Kanal Backend does not know how to provision {str(node)}")

        return pod


