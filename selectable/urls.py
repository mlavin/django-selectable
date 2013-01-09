try:
    from django.conf.urls import handler404, handler500, patterns, url
except ImportError:
    # Django < 1.4
    from django.conf.urls.defaults import handler404, handler500, patterns, url

from selectable import registry


registry.autodiscover()

urlpatterns = patterns('selectable.views',
    url(r'^(?P<lookup_name>[-\w]+)/$', 'get_lookup', name="selectable-lookup"),
)
