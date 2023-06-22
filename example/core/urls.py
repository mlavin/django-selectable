from django.urls import re_path

from .views import advanced, formset, index

urlpatterns = [
    re_path(r"^formset/", formset, name="example-formset"),
    re_path(r"^advanced/", advanced, name="example-advanced"),
    re_path(r"^", index, name="example-index"),
]
