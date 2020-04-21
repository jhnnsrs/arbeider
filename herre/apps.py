from django.apps import AppConfig


class HerreConfig(AppConfig):
    name = 'herre'

    def ready(self):
        import herre.signals