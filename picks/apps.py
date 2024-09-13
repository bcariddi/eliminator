from django.apps import AppConfig


class PicksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'picks'

    def ready(self):
        import picks.signals
