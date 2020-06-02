from delt.bouncers.base import BaseBouncer, BaseBouncerSettings
from delt.bouncers.context import BouncerContext
from delt.models import Pod

class BasePodBouncer(BaseBouncer):

    def __init__(self, pod: Pod, context: BouncerContext):
        self.pod = pod
        super().__init__(context)

    def can_provision(self)-> bool:
        raise NotImplementedError("Please overwrite this in your PodBouncer")

    def can_assign_job(self)-> bool:
        raise NotImplementedError("Please overwrite this in your PodBouncer")
