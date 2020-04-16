import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from delt.fields import SettingsField, ArgsField
from delt.helpers import get_default_job_settings
from delt.status import STATUS_PENDING


class Node(models.Model):
    identifier = models.CharField(max_length=1000, unique=True, editable=False, help_text="A unique identifier of this Node on this Platform, calculated hashing the package and interface")
    variety = models.CharField(max_length=1000, help_text="Is this Node a Frontend, Backend, DaskExlusiv Node?")
    backend = models.CharField(max_length=1000, help_text="The Backend this Node uses")
    package = models.CharField(max_length=1000, help_text="The Package this Node belongs to")
    interface = models.CharField(max_length=1000, help_text="The unique interface of this Node within the Package")
    name = models.CharField(max_length=1000, help_text="The Package that channel belongs to")
    description = models.TextField(help_text="A Short description for the Node")
    settings = SettingsField(max_length=1000, default=dict)  # json decoded standardsettings
    inputs = JSONField(default=list)
    outputs = JSONField(default=list)
    nodeclass = models.CharField(max_length=400, default="classic-node")

    def __str__(self):
        return f"Node {self.name} ( Package: {self.package}/{self.interface}  ) on Identifier {self.identifier}"


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


class Job(models.Model):
    args = ArgsField()
    settings = SettingsField(max_length=1000, default=get_default_job_settings) # jsondecoded
    statuscode = models.IntegerField( default= STATUS_PENDING)
    statusmessage = models.CharField(max_length=500,  default= "Pending")
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    instance = models.CharField(max_length=400, default= uuid.uuid4, help_text="The Nodeinstance this Job lives on")
    selector = models.CharField(max_length=400, default= uuid.uuid4, help_text="The Selectivity for Instances of this Node (especially unique Frontends)")
    unique = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

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
        if not self._state.adding and (
                self.creator_id != self._loaded_values['creator_id']):
            raise ValueError("Updating the value of creator isn't allowed")
        super().save(*args, **kwargs)


    


# Layout and Flow for construction of Graphs
class Flow(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, default="Not Set")
    diagram = JSONField(max_length=50000, help_text="The Charted diagram")
    description = models.CharField(max_length=50000, default="Add a Description")





