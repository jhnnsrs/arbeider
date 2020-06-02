from delt.bouncers.base import BaseBouncerSettings
from delt.bouncers.node.base import BaseNodeBouncer


class AllAccessNodeBouncerSettings(BaseBouncerSettings):
    provider = "all_access"

class AllAccessNodeBouncer(BaseNodeBouncer):
    settingsClass = AllAccessNodeBouncerSettings()
    
    def can_provision_pods(self)-> bool:
        return True

    def can_provide_on(self, provider):
        return True