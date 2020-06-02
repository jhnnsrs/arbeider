from delt.bouncers.base import BaseBouncerSettings
from delt.bouncers.job.base import BaseJobBouncer


class AllAccessJobBouncerSettings(BaseBouncerSettings):
    provider = "all_access"

class AllAccessJobBouncer(BaseJobBouncer):
    settingsClass = AllAccessJobBouncerSettings()

    def can_assign_job(self, pod)-> bool:
        return True