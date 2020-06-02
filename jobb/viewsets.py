import logging

from oauth2_provider.contrib.rest_framework import (TokenHasReadWriteScope,
                                                    TokenHasScope)
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.metadata import SimpleMetadata
from rest_framework.response import Response

from delt.job import JobConfig, job_config_builder
from delt.message import send_to_backend
from delt.models import Job
from delt.context import Context
from delt.node import NodeConfig
from delt.params import Inputs
from delt.serializers import JobSerializer

logger = logging.getLogger(__name__)


class JobRouteMetadata(SimpleMetadata):
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


class JobRouteViewSet(viewsets.ModelViewSet):
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
    metadata_class = JobRouteMetadata

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#
        self.name = self.config.name
    

    @property
    def created_serializer(self):
        if self.config and issubclass(self.config, NodeConfig):

            return job_config_builder(self.node, self.config.inputs)

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
            raise APIException(detail="No Node found on any Backend. Have you installed it or restarted the Server after cataloging it?")

        context = Context(request=request)
        context.is_authorized("")
        serializer = self.created_serializer(data=request.data)
        if serializer.is_valid():

            inputs = serializer.data["inputs"]
            pod = serializer.validated_data["pod"]
            instance = serializer.validated_data["instance"]
            
            job = Job.objects.create(
                args=inputs,
                creator= request.user,
                node = self.node,
                pod = pod,
                instance= serializer.validated_data["instance"],
                )

            serialized = JobSerializer(job)

            try:
                new_job_pipe(job, context)
            except BaseProvisionerError as e:
                raise APIException(detail=f"{e}")

            return Response(serialized.data, status=status.HTTP_201_CREATED)

        else:
            raise APIException(detail="Wrong")