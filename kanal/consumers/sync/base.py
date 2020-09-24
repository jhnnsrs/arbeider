from delt.utils import gateway_send
from delt.consumers import gateway
from kanal.utils import layer_send
from konfig.node import Konfig
from delt.consumers.utils import deserialized
import logging

from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from rest_framework import serializers

from delt.models import Job
from delt.serializers import AssignationMessageSerializer, JobSerializer
from kanal.exceptions import KanalConsumerConfigException, KanalConsumerMinorException

logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()

def getJob(id, model):
    return model.objects.get(id=id)

def updateJob(job: Job, message):
    job.statusmessage = message
    job.save()
    return job

class KanalSyncConsumer(SyncConsumer):
    konfig: Konfig  = None
    jobSerializer = JobSerializer

    def __init__(self, scope):
        if self.konfig is None or not issubclass(self.konfig, Konfig):
            print("Something going wrong")
            raise KanalConsumerConfigException(f"{self.__class__.__name__} was not registered with a Node")

        super().__init__(scope)


    def progress(self, message):
        logger.info("Progress", message)
        self.assignation.status = f"progress: {message}"
        self.assignation.save()

        serialized = AssignationMessageSerializer({"assignation": self.assignation})
        gateway_send("assignation_progress")(serialized.data)

    @deserialized(AssignationMessageSerializer)
    def assign(self, message ):
        self.assignation = message["assignation"]
        inputs: serializers.Serializer = self.konfig.inputs(data=self.assignation.inputs)
        if inputs.is_valid(raise_exception=True):
            try:
                outputdict = self.start(inputs.validated_data)

                # Serialize the outputs
                outputs = self.konfig.outputs(outputdict)
                self.assignation.status = "done"
                self.assignation.outputs = outputs.data
                self.assignation.save()
                # Send them Back
                serialized = AssignationMessageSerializer({"assignation": self.assignation})
                gateway_send("assignation_done")(serialized.data)
            except KanalConsumerMinorException as e:
                logger.error(e)
                if settings.DEBUG:
                    raise e
        

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


    def updateJob(self, message):
        # Classic Update Circle
        self.job = updateJob(self.job, message)
        self.publish(self.job, self.jobSerializer, update=True)


    def start(self, inputs: dict):
        """ 
        Should Return the outputs as a dict

        """
        raise NotImplementedError


    @property
    def settings(self):
        return {} #TODO: Implement

