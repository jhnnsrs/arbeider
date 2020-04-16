STATUS_PENDING= 1500
STATUS_STARTED = 2000
STATUS_DONE = 1000
STATUS_PROGRESS = 3000
STATUS_ERROR = 4000
STATUS_WARNING = 5000


class StatusCode(object):
    PENDING = STATUS_PENDING
    STARTED = STATUS_STARTED
    DONE = STATUS_DONE
    PROGRESS = STATUS_PROGRESS
    ERROR = STATUS_ERROR
    WARNING = STATUS_WARNING


class Messages(object):
    STARTED = "Starting"
    ERROR = "Error"
    PROGRESS = "Progress"
    DONE = "Done"

    @staticmethod
    def error(message) -> str:
        return Messages.ERROR + " - " + str(message)

    @staticmethod
    def progress(percent) -> str:
        return Messages.PROGRESS + " - " + str(percent)


class JobStatus(object):

    def __init__(self,code: int, message: str = None):
        self.statuscode = code
        self.message = message if message is not None else ""


def buildErrorStatus(message = None):
    return JobStatus(StatusCode.ERROR,message)

def buildWarningStatus(message = None):
    return JobStatus(StatusCode.WARNING,message)

def buildProgressStatus(message = None):
    return JobStatus(StatusCode.PROGRESS,message)


def buildDoneStatus(message = None):
    return JobStatus(StatusCode.DONE,message)