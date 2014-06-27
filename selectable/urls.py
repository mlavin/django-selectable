from django.conf.urls import url

from . import registry
from . import views


registry.autodiscover()


urlpatterns = [
    url(r'^(?P<lookup_name>[-\w]+)/$', views.get_lookup, name="selectable-lookup"),
]
