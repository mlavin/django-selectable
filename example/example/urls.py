#from django.conf.urls import include, url
from django.urls import include
from django.urls import re_path as url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^', include('core.urls')),
]
