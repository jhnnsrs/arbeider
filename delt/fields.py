from django.contrib.postgres.fields.jsonb import JSONField


class SettingsField(JSONField):
    pass


class ArgsField(JSONField):
    pass