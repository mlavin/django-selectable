from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^', include('core.urls')),
]
