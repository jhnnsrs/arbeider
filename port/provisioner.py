import logging
import re
import uuid

from guardian.shortcuts import assign_perm
from balder.utils import serializerToDict
from delt import selector as selectors
from delt.consumers.exceptions import NoMatchablePod
from delt.consumers.job import JobConsumer
from delt.consumers.provisioner import ProvisionConsumer
from delt.consumers.utils import deserialized
from delt.models import Job, Provision, Pod
from delt.pod import PODPENDING
from delt.serializers import JobSerializer, PodSerializer
from delt.settingsregistry import get_settings_registry
from extensions.fremmed.subscriptions import GateSubscription
from port.models import Flowly
import docker 

logger = logging.getLogger(__name__)

class PortProvisionError(Exception):
    pass

DRYRUN = True

class FakeContainer(object):
    id: str

    def __init__(self, id = "nananana"):
        self.id = id

def spawnContainerForProvision(provision: Provision) -> str:
    client = docker.from_env()
    logger.info("Trying to spawn a docker container")

    container = client.containers.run("jhnnsrs/flowango", detach=True, environment={"PROVISION_ID": provision.id }, network="dev")

    return container


class PortProvision(ProvisionConsumer):
    provider = "port"

    def get_pod(self, provision):
        logger.info(f"Received {provision}")

        # Are we provisioning a Flow???
        flow = provision.node.flownode
        if flow is None: raise NotImplementedError("We are still only able to provision FLOWS")


        node = provision.node
        if selectors.all(provision.subselector):
            pod = Flowly.objects.filter(node=provision.node).first()
            if not pod:
                logger.info("No Pod with this configuration yet found")
                if provision.user:
                    pod = Flowly.objects.create(
                        node = flow,
                        podclass = "flow",
                        status = PODPENDING,
                        provider = self.provider,
                        persistent = False
                    )

                    provision.pod = pod

                    container = spawnContainerForProvision(provision)
                    pod.container_id = container.id
                    pod.save()
                else:
                   raise PortProvisionError("Only signed in users are allowed to create Pods")


        if selectors.new(provision.subselector):
            if provision.user:
                    pod = Flowly.objects.create(
                        node = flow,
                        podclass = "flow",
                        status = PODPENDING,
                        provider = self.provider,
                        persistent = False
                    )
                    
                    provision.pod = pod

                    container = spawnContainerForProvision(provision)
                    pod.container_id = container.id
                    pod.save()
            else:
                raise PortProvisionError("Only signed in users are allowed to create Pods")

        logger.info(f"Created POD with ID: {pod.container_id}")
        logger.info(f"Created POD with FLOW: {pod.node_id}")
        logger.info(f"Created POD with PROVISION: {provision.id}")
        return pod
