#from django.conf.urls import url
from django.urls import re_path as url

from . import views


urlpatterns = [
    url(r'^(?P<lookup_name>[-\w]+)/$', views.get_lookup, name="selectable-lookup"),
]
