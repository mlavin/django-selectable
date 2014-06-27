try:
    from django.apps import AppConfig
except ImportError:
    AppConfig = object


class SelectableConfig(AppConfig):
    """App configuration for django-selectable."""

    name = 'selectable'

    def ready(self):
        self.module.registry.autodiscover()
