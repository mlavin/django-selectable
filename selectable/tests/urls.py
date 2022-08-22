#from django.conf.urls import handler404, handler500, include, url
from django.conf.urls import handler404, handler500
from django.urls import include
from django.urls import re_path as url


handler404 = 'selectable.tests.views.test_404'
handler500 = 'selectable.tests.views.test_500'

urlpatterns = [
    url(r'^selectable-tests/', include('selectable.urls')),
]
