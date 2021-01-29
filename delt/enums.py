from enum import Enum


def enumToChoices(enum: Enum):
    return [(tag.value, tag.value) for tag in enum]



class ExceptionType(str, Enum):
    CLIENT = "client"
    ARNHEIM = "arnheim"
    PROVIDER = "provider"
    POD = "pod"


class ClientType(str, Enum):
    EXTERNAL = "external"
    INTERNAL = "internal"
    LOCAL = "local"
    USER = "user"
    ADMIN = "admin"



class Endpoint(str, Enum):
    GRAPHQL = "graphql"
    REST = "rest"
    


class PodStatus(str, Enum):
    DOWN = "DOWN"
    ERROR = "ERROR"
    PENDING = "PENDING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    ACTIVE = "ACTIVE"


class AssignationStatus(str, Enum): 
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    YIELD = "YIELD"
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