from delt.utils import generate_random_name
from delt.integrity import node_identifier
from typing import Iterable, Optional
from delt.managers import PodManager
import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from delt.fields import (AccessPolicy, ArgsField, InputsField, OutputsField,
                         PublishersField, SelectorField, SettingsField)
from delt.helpers import get_default_job_settings
from delt.constants.lifecycle import JOB_PENDING, POD_PENDING
import logging


import django.db.models.options as options


logger = logging.getLogger(__name__)


logger.info("Adding identifiers to Meta class")
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('identifiers',)



class Provider(models.Model):
    ''' The Provider is a model to show what templates belong to '''
    name = models.CharField(max_length=1000, help_text="This Providers Name")
    installed_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self) -> str:
        return self.name


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
    repository = models.ForeignKey(Repository, null=True, blank=True, on_delete=models.CASCADE)

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
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True,null=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, help_text="The Node this Template Belongs to", related_name="templates")
    name = models.CharField(max_length=1000, default=generate_random_name, help_text="The name of this template")
    version = models.CharField(max_length=400, help_text="A short descriptor for the kind of version") #Subject to change

    def __str__(self):
        return f"Template of {self.node.name} on {self.provider.name} "


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
    node = models.ForeignKey(Node, on_delete=models.CASCADE, help_text="The node this Pod is an instance of", related_name="pods")
    template = models.ForeignKey(Template, on_delete=models.CASCADE, help_text="The template used to create this pod", related_name="pods", null=True, blank=True)
    podclass = models.CharField(max_length=400, default="classic-pod")
    status = models.CharField(max_length=300, default= POD_PENDING)
    provider = models.CharField(max_length=1000, help_text="The provisioner that created this Pod")
    unique = models.UUIDField(max_length=1000, unique=True, default=uuid.uuid4, help_text="The Unique identifier of this POD")
    reference = models.CharField(max_length=1000, unique=True, null=True, blank=True,  help_text="The Unique identifier of this POD")
    persistent = models.BooleanField(default=False)
    policy = models.CharField(max_length=5000, default= "*")


    objects = PodManager()

    def __str__(self):
        return f"Pod for node {self.node.name} ( Package: {self.node.package}/{self.node.interface}  ) at {self.provider}"

    def assign(self, assignation):
        raise NotImplementedError("Your Pod must provide a interface how to assign a Job to It")

class Provision(models.Model):
    """ A Provision constitutes a way of providing an Instance of an Implementation """
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, help_text="The Provisions parent", related_name="children")
    node = models.ForeignKey(Node, on_delete=models.CASCADE, help_text="The node this provision connects", related_name="provisions")
    template = models.ForeignKey(Template, on_delete=models.CASCADE, help_text="The template used to create this provision", related_name="provisions", null=True, blank=True)
    pod = models.ForeignKey(Pod, on_delete=models.CASCADE, help_text="The pod this provision connects", related_name="provisions", null=True, blank=True)
    active = models.BooleanField(default=False)
    provider = models.CharField(max_length=1000, help_text="The Provider")
    subselector = models.CharField(max_length=1000, help_text="The selector")
    token = models.CharField(max_length=1000, blank=True, default=uuid.uuid4(), help_text="The Token that created this Provision")
    reference = models.CharField(max_length=1000, unique=True, default=uuid.uuid4, help_text="The Unique identifier of this Provision")
    status = models.CharField(max_length=1000, blank=True, help_text="This provisions status")
    statusmessage = models.CharField(max_length=1000, blank=True, help_text="This provisions status")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, max_length=1000, help_text="This provision creator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Job(models.Model):
    """ 
    A Job is the Arnheim equivalent of a Task that lives on a Node
    """
    inputs = InputsField(blank=True, null=True, help_text="The Inputs")
    outputs = OutputsField(help_text="The Outputs", blank=True, null=True)
    settings = SettingsField(max_length=1000, default=get_default_job_settings) # jsondecoded
    status = models.CharField(max_length=500,  default= JOB_PENDING)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pod = models.ForeignKey(Pod, on_delete=models.CASCADE, null=True, blank=True, help_text="The Pod this Job lives on")
    reference = models.CharField(max_length=400, default= uuid.uuid4, help_text="The Nodeinstance this Job lives on")
    selector = SelectorField(max_length=400, blank=True, help_text="The Selectivity for Instances of this Node (especially unique Frontends)")
    unique = models.UUIDField(max_length=1000, unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Request by {self.creator.username}"

    def _repr_html_(self):
        return f'''<h5>Request by {self.creator.username} </h5>
                <ul>
                    <li> Last Status: {self.statusmessage}</li>
                    <li> Node Status: {self.nodeid}</li>
                    <li> Settings: {self.settings}</li>
                </ul>'''

    def save(self, *args, **kwargs):
        # Check how the current values differ from ._loaded_values. For example,
        # prevent changing the creator_id of the model. (This example doesn't
        # support cases where 'creator_id' is deferred).
        super().save(*args, **kwargs)

    class Meta:
        permissions = (
                ('queue_job', 'Queue Job'),
            )

class Assignation(models.Model):
    pod = models.ForeignKey(Pod, on_delete=models.CASCADE, help_text="The pod this provision connects", related_name="assignations")
    inputs = InputsField(blank=True, null=True, help_text="The Inputs")
    outputs = OutputsField(help_text="The Outputs", blank=True, null=True)
    reference = models.CharField(max_length=1000, unique=True, default=uuid.uuid4, help_text="The Unique identifier of this Provision")
    status = models.CharField(max_length=1000, help_text="This provisions status")
    message = models.CharField(max_length=1000, help_text="This provisions status")
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=1000, blank=True, default=uuid.uuid4(), null=True, help_text="The Token that created this Provision")

    def __str__(self) -> str:
        return f"Assignation {self.id} on (ref: {self.reference}) for {self.pod} "
    
    