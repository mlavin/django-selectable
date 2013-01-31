from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.utils.importlib import import_module

from selectable.compat import string_types


__all__ = (
    'BaseLookupForm',
    'import_lookup_class',
)


class BaseLookupForm(forms.Form):
    term = forms.CharField(required=False)
    limit = forms.IntegerField(required=False, min_value=1)
    page = forms.IntegerField(required=False, min_value=1)

    def clean_limit(self):
        "Ensure given limit is less than default if defined"
        limit = self.cleaned_data.get('limit', None)
        if (settings.SELECTABLE_MAX_LIMIT is not None and
            (not limit or limit > settings.SELECTABLE_MAX_LIMIT)):
            limit = settings.SELECTABLE_MAX_LIMIT
        return limit

    def clean_page(self):
        "Return the first page if no page or invalid number is given."
        return self.cleaned_data.get('page', 1) or 1


def import_lookup_class(lookup_class):
    """
    Import lookup_class as a dotted base and ensure it extends LookupBase
    """
    from selectable.base import LookupBase
    if isinstance(lookup_class, string_types):
        mod_str, cls_str = lookup_class.rsplit('.', 1)
        mod = import_module(mod_str)
        lookup_class = getattr(mod, cls_str)
    if not issubclass(lookup_class, LookupBase):
        raise TypeError('lookup_class must extend from selectable.base.LookupBase')
    return lookup_class
