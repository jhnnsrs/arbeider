import logging

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer
from rest_framework import serializers

from delt.consumers.utils import deserialized
from delt.context import Context
from delt.models import Job, Node, Pod
from delt.serializers import AssignationSerializer

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()

class JobConsumer(SyncConsumer):

    @deserialized(AssignationSerializer)
    def on_assign_job(self, data):
        reference = data["reference"]
        pod = data["pod"]
        inputs = data["inputs"]
        user = data["user"]
        self.assign_job(reference, pod, inputs, user)

    def assign_job(self, reference, pod, args, user):
        raise NotImplementedError("Please derived a assign_job class in your consumer")
