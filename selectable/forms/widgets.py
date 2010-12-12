from django import forms
from django.conf import settings


__all__ = (
    'AutoCompleteWidget',
    'AutoCompleteSelectWidget',
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


class AutoCompleteSelectWidget(forms.MultiWidget):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        widgets = [
            AutoCompleteWidget(lookup_class, allow_new=self.allow_new),
            forms.HiddenInput(attrs={u'data-selectable-is-hidden': 'true'})
        ]
        super(AutoCompleteSelectWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            lookup = self.lookup_class()
            item = lookup.get_item(value)
            item_value = lookup.get_item_value(item)
            return [item_value, value]
        return [None, None]

