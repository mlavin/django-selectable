from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('selectable/', include('selectable.urls')),
    path('', include('core.urls')),
]
