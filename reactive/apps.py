from django.apps import AppConfig


class ReactiveConfig(AppConfig):
    name = 'reactive'

    def ready(self) -> None:
        return super().ready()
