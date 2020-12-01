import graphene

class PodStatus(graphene.Enum):
    ERROR = 1
    INFO = 2
    DEBUG = 3

    @property
    def description(self):
        if self == PodStatus.ERROR:
            return 'Error Status'
        return 'Other Status'