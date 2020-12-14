from enum import Enum


def enumToChoices(enum: Enum):
    return [(tag, tag.value) for tag in enum]



class ClientType(str, Enum):
    EXTERNAL = "external"
    USER = "user"
    ADMIN = "admin"



class Endpoint(str, Enum):
    GRAPHQL = "graphql"
    REST = "rest"
    


class PodStatus(str, Enum):
    ERROR = "ERROR"
    PENDING = "PENDING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    ACTIVE = "ACTIVE"


class AssignationStatus(str, Enum): 
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    DENIED = "ASSIGNED"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    PROGRESS = "PROGRESS"
    DEBUG = "DEBUG"
    DONE = "DONE"


class ProvisionStatus(str, Enum): 
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    DENIED = "ASSIGNED"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    PROGRESS = "PROGRESS"
    DEBUG = "DEBUG"
    DONE = "DONE"