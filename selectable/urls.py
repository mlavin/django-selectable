from django.conf.urls import url

from . import views
from .compat import LEGACY_AUTO_DISCOVER 

if LEGACY_AUTO_DISCOVER:
    # Auto-discovery is now handled by the app configuration
    from . import registry

    registry.autodiscover()


urlpatterns = [
    url(r'^(?P<lookup_name>[-\w]+)/$', views.get_lookup, name="selectable-lookup"),
]
