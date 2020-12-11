from django.db.models import CharField, JSONField
from rest_access_policy.access_policy import AccessPolicy


# Composed NodeFields
class InputsField(JSONField):
    pass

# Composed NodeFields
class OutputsField(JSONField):
    pass

# Kwargs are Types that allow the Provider to specify the shape of a request to them
class KwargsField(JSONField):
    pass # 

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