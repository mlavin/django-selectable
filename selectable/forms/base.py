from django import forms
from django.conf import settings


__all__ = ('BaseLookupForm', )


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
