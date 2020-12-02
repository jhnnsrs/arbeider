from django.apps import AppConfig


class AutoProviderConfig(AppConfig):
    name = 'providers.auto'


    def ready(self):
        pass
