from delt.enums import Endpoint, enumToChoices
from delt.utils import generate_random_name
from delt.integrity import node_identifier
from typing import Iterable, Optional
from delt.managers import PodManager
import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from delt.fields import (AccessPolicy, ArgsField, InputsField, KwargsField, OutputsField,
                         PublishersField, SelectorField, SettingsField)
from delt.helpers import get_default_job_settings
from delt.constants.lifecycle import JOB_PENDING, POD_PENDING
import logging


import django.db.models.options as options


logger = logging.getLogger(__name__)


logger.info("Adding identifiers to Meta class")
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('identifiers',)






class Provider(models.Model):
    ''' Providers are extending the functionality as plugins:
    You can use the provider to provision pods and implement a custom assignation logic
    
    A provider implements a handler that gets called by the provision pipe and can
    override SelectorKwargs to enable autocompletion of the required models
    '''
    name = models.CharField(max_length=1000, help_text="This Providers Name")
    installed_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self) -> str:
        return f"Provider: {self.name}"


class DataPoint(models.Model):
    """A Datapoint is the way arnheim is allowing access to apis, a datapoint stores the protocol

    """
    host = models.CharField(max_length=100, help_text="Where are we storing this??")
    name = models.CharField(max_length=100, help_text="A unique identifier for this datapoint, will be prepeneded to the Model it hosts", unique=True)
    port = models.IntegerField(help_text="the port this point lives on")
    type = models.CharField(max_length=100, choices=enumToChoices(Endpoint), help_text="The Type of API")
    installed_at = models.DateTimeField(auto_created=True, auto_now_add=True)



class DataModel(models.Model):
    """ A unique serverside model to interact with , it lives on a datapoint"""
    point = models.ForeignKey(DataPoint, on_delete=models.CASCADE, related_name="models")
    identifier = models.CharField(max_length=100, help_text=" A unique identifier for this model in its Datapoint")
    installed_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    extenders = models.JSONField(null=True, blank=True, help_text="Unique identifiers for a Datamodel, good for introspection")



class ProviderSettings(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, help_text="The implemented Provider!")
    active = models.BooleanField(default=True, help_text="Is this provider active or no longer active?")
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)



class Repository(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, help_text="The Person that created this repository")
    name = models.CharField(max_length=1000, help_text="A unique identifier of this Repository on this Platform, calculated hashing the package and interface")
    type = models.CharField(max_length=300, help_text="What sort of repository is this")

    def __str__(self) -> str:
        return self.name

class Node(models.Model):
    identifier = models.CharField(max_length=1000, unique=True, editable=False, help_text="A unique identifier of this Node on this Platform, calculated hashing the package and interface")
    variety = models.CharField(max_length=1000, help_text="Is this Node a Frontend, Backend, DaskExlusiv Node?")
    realm = models.CharField(max_length=1000, help_text="The realm this Node was registered to?")
    package = models.CharField(max_length=1000, help_text="The Package this Node belongs to")
    interface = models.CharField(max_length=1000, help_text="The unique interface of this Node within the Package")
    publishers = PublishersField(help_text="The publishers thie Node will send to",default=dict)
    name = models.CharField(max_length=1000, help_text="The Package that channel belongs to")
    description = models.TextField(help_text="A Short description for the Node")
    image = models.ImageField(null=True, blank=True)
    inputs = InputsField(default=list)
    outputs = OutputsField(default=list)
    nodeclass = models.CharField(max_length=400, default="classic-node")
    repository = models.ForeignKey(Repository, null=True, blank=True, on_delete=models.CASCADE, related_name="nodes")

    def save(self,*args, **kwargs) -> None:
        logger.info(f"Validating Integrity of {str(self)}")
        if not self.identifier:
            self.identifier = node_identifier(self.package,self.interface)
        return super().save(*args, **kwargs)

    def get_identifier(self):
        return self.identifier

    def __str__(self):
        return f"Node {self.name} ( Package: {self.package}/{self.interface}  ) on Identifier {self.identifier}"


class Template(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, help_text="The Node this Template Belongs to", related_name="templates")
    name = models.CharField(max_length=1000, default=generate_random_name, help_text="The name of this template")

    # Meta Field
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    version = models.CharField(max_length=400, help_text="A short descriptor for the kind of version") #Subject to change
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Template of {self.node.name} "


class Route(models.Model):
    identifier = models.CharField(max_length=1000, unique=True, editable=False, help_text="A unique identifier of this Route on this Platform, calculated hashing the package and interface")
    url = models.URLField(max_length=1000, help_text="The url to the Route")
    package = models.CharField(max_length=1000, help_text="The Package this Node belongs to")
    provider = models.CharField(max_length=1000, help_text="The Provider of this Route")
    interface = models.CharField(max_length=1000, help_text="The unique interface of this Node within the Package")
    name = models.CharField(max_length=1000, help_text="The Package that channel belongs to")
    description = models.TextField(help_text="A Short description for the Node")
    node = models.ForeignKey(Node, blank=True, null=True, related_name="routes", on_delete=models.CASCADE)

    def __str__(self):
        return f"Node {self.name} ( Package: {self.package}/{self.interface}  ) on Identifier {self.identifier}"


class Pod(models.Model):
    """ A Pod is Arnheims Representation of an Instance of an Implementation of a Node"""
    template = models.ForeignKey(Template, on_delete=models.CASCADE, help_text="The template used to create this pod", related_name="pods")
    podclass = models.CharField(max_length=400, default="classic-pod")
    status = models.CharField(max_length=300, default=POD_PENDING)
    unique = models.UUIDField(max_length=1000, unique=True, default=uuid.uuid4, help_text="The Unique identifier of this POD")
    policy = models.CharField(max_length=5000, default= "*")


    objects = PodManager()

    def __str__(self):
        return f"Pod for Template {self.template} at {self.template.provider}"

    def assign(self, assignation):
        raise NotImplementedError("Your Pod must provide a interface how to assign a Job to It")

class Provision(models.Model):
    """ A Provision constitutes a way of providing an Instance of an Implementation """

    # 1. Input to the Provision
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, help_text="The Provisions parent", related_name="children")
    node = models.ForeignKey(Node, on_delete=models.CASCADE, help_text="The node this provision connects", related_name="provisions")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, help_text="The provider we might want")
    kwargs = models.JSONField(null=True, blank=True, help_text="Kwargs for the Provider") 
    reference = models.CharField(max_length=1000, unique=True, default=uuid.uuid4, help_text="The Unique identifier of this Provision")
    


    # 2. Getting the Pod 
    pod = models.ForeignKey(Pod, on_delete=models.CASCADE, help_text="The pod this provision connects", related_name="provisions", null=True, blank=True)
    
    # Status fields
    status = models.CharField(max_length=1000, blank=True, help_text="This provisions status")
    statusmessage = models.CharField(max_length=1000, blank=True, help_text="This provisions status")


    # Meta fields 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, max_length=1000, help_text="This provision creator")
    token = models.CharField(max_length=1000, blank=True, default=uuid.uuid4(), help_text="The Token that created this Provision") # TODO: Get rid of this???


class Assignation(models.Model):

    # 1. Input to the Assignation
    pod = models.ForeignKey(Pod, on_delete=models.CASCADE, help_text="The pod this provision connects", related_name="assignations")
    inputs = InputsField(blank=True, null=True, help_text="The Inputs")
    reference = models.CharField(max_length=1000, unique=True, default=uuid.uuid4, help_text="The Unique identifier of this Assignation")


    # 2. Input to the Provision
    status = models.CharField(max_length=1000, help_text="This assignations status")
    statusmessage = models.CharField(max_length=1000, blank=True, help_text="This assignation status message")


    # 2. The Termination of the Assignation
    outputs = OutputsField(help_text="The Outputs", blank=True, null=True)


    # Meta fields 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, max_length=1000, help_text="This provision creator")
    token = models.CharField(max_length=1000, blank=True, default=uuid.uuid4(), help_text="The Token that created this Provision") # TODO: Get rid of this???

    def __str__(self) -> str:
        return f"Assignation {self.id} on (ref: {self.reference}) for {self.pod} "
    
    class Meta:
        permissions = (
                ('can_assign', 'Assign Job'),
            )

class Selector(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, help_text="The provider these kwargs belong to", related_name="selectors")
    kwargs = KwargsField(blank=True, null=True, help_text="The Specific inputs this selector needs and their types")


    def __str__(self) -> str:
        return f"Selector for {self.provider}"