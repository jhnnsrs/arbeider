import logging
from delt.models import Job
from django.conf import settings

logger = logging.getLogger(__name__)


class BasePublisherError(Exception):
    pass


class BasePublisherConfigError(BasePublisherError):
    pass

class BasePublisherSettings(object):
    settingsField = "PUBLISHERS"

    def __init__(self, **kwargs):
        if self.settingsField is None or self.provider is None:
            raise NotImplementedError("Please Provide provider and settingsField in your Register Settings")
        #Set Defaults from config
        if hasattr(settings, self.settingsField):
            providers = getattr(settings,self.settingsField)
            if self.provider in providers:
                for key, value in providers[self.provider].items():
                    logger.info(f"Overwriting {key} with {value} at {self.provider} in {self.settingsField}")
                    setattr(self,key,value)


class BasePublisher(object):

    def __init__(self):
        super().__init__()


    def on_job_created(self, job: Job):
        logger.info(f"Created Job: {str(job)}")


    def on_job_updated(self, job: Job):
        logger.info(f"Uppdated Job: {str(job)}")

