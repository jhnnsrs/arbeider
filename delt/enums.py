from enum import Enum


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