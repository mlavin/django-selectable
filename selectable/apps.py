try:
    from django.apps import AppConfig
except ImportError:
    AppConfig = object


class SelectableConfig(AppConfig):
    """App configuration for django-selectable."""

    name = 'selectable'

    def ready(self):
        from . import registry
        registry.autodiscover()
