from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^selectable-tests/', include('selectable.urls')),
)
