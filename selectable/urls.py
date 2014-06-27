from django import get_version
from django.conf.urls import url

from . import views


if get_version() < (1, 7):
    # Auto-discovery is now handled by the app configuration
    from . import registry

    registry.autodiscover()


urlpatterns = [
    url(r'^(?P<lookup_name>[-\w]+)/$', views.get_lookup, name="selectable-lookup"),
]
