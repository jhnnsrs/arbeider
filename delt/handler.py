import logging

from prometheus_client.decorator import contextmanager

from delt.job import JobContext
from delt.models import Job, Pod
from delt.provisioner import BaseProvisioner
from delt.settingsregistry import get_settings_registry

logger = logging.getLogger(__name__)


class BaseHandlerException(Exception):
    pass

class BaseHandlerConfigException(Exception):
    pass

class BaseHandler():
    provisioner = BaseProvisioner()

    def __init__(self):
        logger.info(f"Registering Handler {self.__class__.__name__}")
        super().__init__()



    def on_job(self, job: Job, context: JobContext):
        """Specifiy Handling Requests here
        
        Arguments:
            job {Job} -- The Job that was passed by a Route
            context {JobContext} -- The Job that was passed by a Route
    

        Returns:
            job {Job} -- Should return the job
        """
        pod = self.provisioner.get_pod(job, context)
        return self.send_job(job, pod)


    def send_job(job: Job, pod: Pod):
        raise NotImplementedError



    def on_outputs(self, outputs: dict, publishers: dict):
        """ Call this """
        return get_settings_registry().getPublishers(publishers).publish(outputs)