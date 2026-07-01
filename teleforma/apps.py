from django.apps import AppConfig


class TeleformaConfig(AppConfig):
    name = "teleforma"
    verbose_name = "Teleforma"

    def ready(self):
        from . import postman_patches  # noqa: F401
