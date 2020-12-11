from delt.handlers.env import BaseHandlerEnvironment
from delt.handlers.protocol import Protocol
from delt.selector import Selector
from delt.models import Node, Pod
from delt.handlers.newbase import BaseHandler
from balder.delt.enums import PodStatus
from port.models import PortSettings
import logging
from port.selector import PortSelector

logger = logging.getLogger(__name__)

class PortProtocol(Protocol):
    pass

class PortHandlerEnv(BaseHandlerEnvironment[PortSettings, PortSelector]):
    settingsModel = PortSettings
    selectorClass = PortSelector

class PortHandler(BaseHandler):
    env = PortHandlerEnv("port")

    def provide(self, node: Node, selector: Selector) -> Pod:
        if selector.is_all():

            
            

            # Lets check if there is already a running instance of this Pod? Maybe we can use that template?
            volunteer = Volunteer.objects.filter(node=node, active=True).first()
            pod = VartPod.objects.create(volunteer=volunteer, node=node, provider=self.settings.provider_name)
            pod.status = PodStatus.PENDING.value
            pod.save()
        else:
            raise NotImplementedError("We haven't implemented that yet")    

        logger.info(f"Created POD with Volunteer: {pod.volunteer_id}")
        # We are asking the queued Volunteer if he is accepting the Task
        return pod