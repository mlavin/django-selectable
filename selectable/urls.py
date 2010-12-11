from django.conf.urls.defaults import *

from selectable import registry


registry.autodiscover()

urlpatterns = patterns('selectable.views',
    url(r'^(?P<lookup_name>[-\w]+)/$', 'get_lookup', name="selectable-lookup"),
)
