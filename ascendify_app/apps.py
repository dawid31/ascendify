from django.apps import AppConfig


class AscendifyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ascendify_app'

    def ready(self):
        import ascendify_app.signals
