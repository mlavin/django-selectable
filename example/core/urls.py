from django.conf.urls.defaults import *


urlpatterns = patterns('example.core.views',
    url(r'^advanced/', 'advanced', name='example-advanced'),
    url(r'^', 'index', name='example-index'),
)
