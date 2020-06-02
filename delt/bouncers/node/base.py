from delt.bouncers.base import BaseBouncer, BaseBouncerSettings
from delt.bouncers.context import BouncerContext
from delt.models import Node

class BaseNodeBouncer(BaseBouncer):

    def __init__(self, node: Node, context: BouncerContext):
        self.node = node
        super().__init__(context)

    def can_provision_pods(self)-> bool:
        raise NotImplementedError("Please overwrite this in your PodBouncer")

    def can_provide_on(self, provider)-> bool:
        raise NotImplementedError("Please overwrite this in your PodBouncer")