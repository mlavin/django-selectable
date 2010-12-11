from django import forms
from django.conf import settings


__all__ = (
    'AutoCompleteWidget',
)


class AutoCompleteWidget(forms.TextInput):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)
        # New attrs
        url = lookup_class.url()
        self.attrs[u'data-selectable-url'] = url
        self.attrs[u'data-selectable-allow-new'] = str(self.allow_new).lower()

