from django.apps import AppConfig


class SelectableConfig(AppConfig):
    """App configuration for django-selectable."""

    name = 'selectable'

    def ready(self):
        from . import registry
        registry.autodiscover()
