from django.conf.urls.defaults import *


urlpatterns = patterns('example.core.views',
    url(r'^', 'index', name='example-index'),
)
