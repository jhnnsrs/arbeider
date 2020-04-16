import logging

from delt.settingsregistry import get_settings_registry

logger = logging.getLogger(__name__)

class BaseHandler():

    def __init__(self):
        logger.info(f"Registering Handler {self.__class__.__name__}")
        super().__init__()

    def on_job(self, job):
        """Specifiy Handling Requests here
        
        Arguments:
            job {Job} -- The Job that was passed by a Route
        
        Raises:
            NotImplementedError: Please override this Method

        Returns:
            job {Job} -- Should return the job
        """
        raise NotImplementedError("Please specifiy a on_job Method in your Handler")


    def on_outputs(self, outputs: dict, publishers: dict):
        """ Call this """
        return get_settings_registry().getPublishers(publishers).publish(outputs)