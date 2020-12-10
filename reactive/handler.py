from port.models import Container, PortPod
from delt.handlers.env import BaseHandlerEnvironment
from delt.handlers.protocol import Protocol
from delt.selector import Selector
from delt.models import Node, Pod
from reactive.models import RxGraph, RxPod, RxSettings, RxTemplate
from delt.handlers.newbase import BaseHandler
from delt.handlers.exceptions import HandlerException
from balder.delt.enums import PodStatus
import logging
import docker
from docker.models.containers import Container as DockerContainer

logger = logging.getLogger(__name__)

class PortProtocol(Protocol):
    pass

class PortHandler(BaseHandler):
    podModel = PortPod

    def __init__(self) -> None:
        self.client = docker.from_env()
        super().__init__()


    def provideContainer(self, container: Container, env: dict = {}) -> DockerContainer:

        dockerimage = container.getDockerName()

        container = self.client.containers.run(dockerimage, 
                                    network=self.settings.default_network,
                                    detach=True,
                                    environment=env)

        
        

        return container



    pass

class ReactiveProtocol(PortProtocol):
    pass

class ReactiveEnv(BaseHandlerEnvironment[RxSettings]):
    settingsModel = RxSettings


class NotTemplateFoundError(HandlerException):
    pass

class ReactiveHandler(PortHandler):
    podModel = RxPod
    env = ReactiveEnv("rx")

    def provide(self, node: Node, selector: Selector) -> Pod:
        print(self.settings.engine)
        
        if selector.is_all():
            
            # Get the first template for this 
            template = RxTemplate.objects.filter(node=node).first()
            if template is None: raise NotTemplateFoundError("We have no template for this Node")
            print(self.settings.engine)

            env = {
                "rxgraph" : template.graph
            }

            doccon = self.provideContainer(template.container,env=env)
            pod = PortPod.objects.create(
                node = node,
                container_id = doccon.id 
            )  
            return pod 
            
        else:
            raise NotImplementedError("We haven't implemented that yet")    
