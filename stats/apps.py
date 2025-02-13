from django.apps import AppConfig


class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
