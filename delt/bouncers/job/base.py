from delt.bouncers.base import BaseBouncer, BaseBouncerSettings

class BaseJobBouncer(BaseBouncer):

    def can_assign_job(self, pod)-> bool:
        raise NotImplementedError("Please overwrite this in your PodBouncer")




