from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'API типографии'

    def ready(self) -> None:
        import api.models_cms  # noqa: F401
