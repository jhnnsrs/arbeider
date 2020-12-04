import graphene

class PodStatus(graphene.Enum):
    ERROR = "ERROR"
    PENDING = "PENDING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    ACTIVE = "ACTIVE"

    @property
    def description(self):
        if self == PodStatus.ERROR:
            return 'Error Status'
        return 'Other Status'



class AssignationStatus(graphene.Enum):
    PENDING = "PENDING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    PROGRESS = "PROGRESS"
    DEBUG = "DEBUG"
    DONE = "DONE"

    @property
    def description(self):
        if self == AssignationStatus.ERROR:
            return 'Error Status'
        return 'Other Status'