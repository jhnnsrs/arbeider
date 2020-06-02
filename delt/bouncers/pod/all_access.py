from delt.bouncers.base import BaseBouncerSettings
from delt.bouncers.pod.base import BasePodBouncer


class AllAccessPodBouncerSettings(BaseBouncerSettings):
    provider = "all_access"

class AllAccessPodBouncer(BasePodBouncer):
    settingsClass = AllAccessPodBouncerSettings()
    
    def can_provision(self)-> bool:
        return True

    def can_assign_job(self):
        return True