import logging

from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from rest_framework import serializers

from delt.models import Job
from delt.node import NodeConfig
from delt.serializers import JobSerializer
from delt.status import buildProgressStatus, JobStatus
from kanal.exceptions import KanalConsumerConfigException, KanalConsumerMinorException

logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()

def getJob(id, model):
    return model.objects.get(id=id)

def updateJob(job: Job, status: JobStatus):
    job.statuscode = status.statuscode
    job.statusmessage = status.message
    job.save()
    return job

class KanalSyncConsumer(SyncConsumer):
    config: NodeConfig  = None
    jobSerializer = JobSerializer

    def __init__(self, scope):
        if self.config is None or not issubclass(self.config, NodeConfig):
            raise KanalConsumerConfigException(f"{self.__class__.__name__} was not registered with a Node")

        super().__init__(scope)


    def progress(self, message):
        self.updateJob(buildProgressStatus(message))

    def getSettings(self):
        """Returns the update settings dict, where defaultsettings where updated with user
        defaults
        
        Returns:
            [dict] -- Updated Settings dict
        """
        oldsettings = {**self.settings}
        newsettings = {**self.job.settings}

        oldsettings.update(newsettings)
        return oldsettings


    def publish(self, model: models.Model, serializer: serializers.Serializer, update=False, delete=False):
        raise NotImplementedError("This is not yet supported")


    def updateJob(self, status: JobStatus):
        # Classic Update Circle
        self.job = updateJob(self.job, status)
        self.publish(self.job, self.jobSerializer, update=True)


    def start(self, inputs: dict):
        """ 
        Should Return the outputs as a dict

        """
        raise NotImplementedError


    def emit_job(self, signal):
        logger.info(f"Received Data on {self.__class__.__name__}")
        data = signal["data"]
        inputs: serializers.Serializer = self.config.inputs(data=data["args"])
        if inputs.is_valid(raise_exception=True):
            try:
                outputdict = self.start(inputs.validated_data)
            except KanalConsumerMinorException as e:
                logger.error(e)
                if settings.DEBUG:
                    raise e
        
        outputs = self.config.outputs(outputdict)
        print(outputs.data)

    @property
    def settings(self):
        return {} #TODO: Implement

