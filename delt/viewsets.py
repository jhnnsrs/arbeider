import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.functional import cached_property
from graphene import Node
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.metadata import BaseMetadata, SimpleMetadata
from rest_framework.response import Response

from delt.exceptions import DeltConfigError
from delt.message import send_to_backend
from delt.models import Job, Node
from delt.params import Inputs, JobConfig, NodeConfig
from delt.serializers import JobSerializer
from due.views import PublishingModelViewSet

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)

class JobPublishingModelViewSet(PublishingModelViewSet):
    register = None # The Registry where this Node was saved
    registerField = None
    publishers = None  # this publishers will be send to the Action Handles and then they can send to the according

    def perform_create(self, serializer):
        """ Right now only the creation of a new Job is possible, no way of stopping a job on its way"""
        serializer.save()
        self.publish_job(serializer)
        self.publish(serializer, "create")

    def publish_job(self, job):
        if self.register or self.registerField is None:
             raise DeltConfigError(f"Please specifiy register and registerField on {self.__class__.__name__}")
        try: 
            node: Node = self.register.objects.get(pk=job.data[self.registerField])
            channel = node.channel

            logger.info("")
            async_to_sync(channel_layer.send)(channel, {"type": "job_in", "job": job.data,
                                                            "publishers": self.publishers})
        except KeyError as e:
            raise DeltConfigError(f"Inproperly configured Job Registry {e}")

class JobMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """
    def determine_metadata(self, request, view):
        return super().determine_metadata(request, view)
        return {
            'name': view.config.__name__,
            'description': view.get_view_description()
        }


class JobViewSet(viewsets.ModelViewSet):
    """ A publishing ViewSet for a Node

    Properties:
        node_conf {NodeConfig} -- A NodeConfig Describing this viewset
        identifier {NodeConfig} -- The channel this listenes to
    
    Arguments:
        viewsets {[type]} -- [description]
    
    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
    
    Returns:
        [type] -- [description]
    """
    queryset = Job.objects.all()
    config = None
    node = None
    inputs_class = None
    settings_class = None
    channel = "maxisp"
    package = None
    interface = None
    permission_classes = [permissions.IsAuthenticated]
    metadata_class = JobMetadata

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#
        self.name = self.config.name
    

    @property
    def created_serializer(self):
        if self.config and issubclass(self.config, NodeConfig):

            class Parsing(JobConfig):
                inputs = self.config.inputs() 

            return Parsing

        if not self.inputs_class or not issubclass(self.inputs_class, Inputs):
            raise NotImplementedError("Please specifiy inputs as Subclass of Inputs")
        # Again, this is a silly example. Don't worry about it, this is
        #   just an example for clarity.
        class Parsing(JobConfig):
            inputs = self.inputs_class()

        return Parsing

    def get_serializer_class(self):
        if self.action == 'create':
            return self.created_serializer
        return JobSerializer

    def list(self, request):
        return Response(data= {"view": "Not Implented"})

    
    def create(self, request):
        if self.node is None:
            raise APIException(detail="No Node found on any Backend")
        serializer = self.created_serializer(data=request.data)
        if serializer.is_valid():
            inputs = serializer.data["inputs"]
            job = Job.objects.create(
                args=inputs,
                creator= request.user,
                node= self.node,
                instance= serializer.validated_data["instance"],
                )

            serialized = send_to_backend(job)

            return Response(serialized.data, status=status.HTTP_201_CREATED)

        else:
            serializer = JobSerializer(data=request.data)
            if serializer.is_valid():
                job = serializer.save()
                serialized = send_to_backend(job)

                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                raise APIException(detail="Wrong")