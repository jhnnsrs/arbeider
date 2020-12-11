from channels.layers import get_channel_layer
from delt.consumers.gateway import channel_layer
from asgiref.sync import async_to_sync
from kanal.handler import KanalHandlerSettings
import logging
import re
import uuid

from guardian.shortcuts import assign_perm

from balder.utils import serializerToDict
from delt import selector as selectors
from delt.consumers.utils import deserialized
from delt.consumers.provisioner import ProvisionConsumer
from delt.consumers.exceptions import NoMatchablePod
from kanal.models import KanalPod

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()

class KanalProvisionConsumer(ProvisionConsumer):
    settings = KanalHandlerSettings()
    provider = "kanal"

    def get_pod(self, provision):
        logger.info(f"Received {provision}")

        node = provision.node
        if selectors.all(provision.subselector):
            pod = KanalPod.objects.filter(node=provision.node).first()
            if not pod:
                raise NoMatchablePod(f"Kanal Backend does not know how to provision {str(node)}")
            
        pod = None
        return pod




