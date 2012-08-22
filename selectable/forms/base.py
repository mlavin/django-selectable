from django import forms
from django.conf import settings


__all__ = ('BaseLookupForm', )

DEFAULT_LIMIT = getattr(settings, 'SELECTABLE_MAX_LIMIT', 25)


class BaseLookupForm(forms.Form):
    term = forms.CharField(required=False)
    limit = forms.IntegerField(required=False, min_value=1)

    def clean_limit(self):
        "Ensure given limit is less than default if defined"
        limit = self.cleaned_data.get('limit', None)
        if DEFAULT_LIMIT and (not limit or limit > DEFAULT_LIMIT):
            limit = DEFAULT_LIMIT
        return limit
