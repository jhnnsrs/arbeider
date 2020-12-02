import graphene

class PodStatus(graphene.Enum):
    ERROR = "error"
    PENDING = "pending"
    INFO = "info"
    DEBUG = "debug"
    ACTIVE = "active"

    @property
    def description(self):
        if self == PodStatus.ERROR:
            return 'Error Status'
        return 'Other Status'