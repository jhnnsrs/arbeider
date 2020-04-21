from django.contrib.postgres.fields.jsonb import JSONField
from django.db.models.fields import CharField
from rest_access_policy.access_policy import AccessPolicy


class SettingsField(JSONField):
    pass


class ArgsField(JSONField):
    pass


class AccessPolicy(JSONField):
    pass

class PublishersField(JSONField):
    pass


class SelectorField(CharField):
    pass