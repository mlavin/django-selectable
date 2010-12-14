from django import forms
from django.conf import settings


__all__ = (
    'AutoCompleteWidget',
    'AutoCompleteSelectWidget',
    'AutoComboboxWidget',
    'AutoComboboxSelectWidget'
)


class AutoCompleteWidget(forms.TextInput):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutoCompleteWidget, self).build_attrs(extra_attrs, **kwargs)
        attrs[u'data-selectable-url'] = self.lookup_class.url()
        attrs[u'data-selectable-type'] = 'text'
        attrs[u'data-selectable-allow-new'] = str(self.allow_new).lower()
        return attrs

class AutoCompleteSelectWidget(forms.MultiWidget):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        widgets = [
            AutoCompleteWidget(lookup_class, allow_new=self.allow_new),
            forms.HiddenInput(attrs={u'data-selectable-type': 'hidden'})
        ]
        super(AutoCompleteSelectWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            lookup = self.lookup_class()
            item = lookup.get_item(value)
            item_value = lookup.get_item_value(item)
            return [item_value, value]
        return [None, None]


class AutoComboboxWidget(AutoCompleteWidget):
    
    def __init__(self, lookup_class, *args, **kwargs):
        super(AutoComboboxWidget, self).__init__(lookup_class, *args, **kwargs)
        self.attrs[u'data-selectable-type'] = 'combobox'

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutoComboboxWidget, self).build_attrs(extra_attrs, **kwargs)
        attrs[u'data-selectable-type'] = 'combobox'
        return attrs


class AutoComboboxSelectWidget(forms.MultiWidget):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        widgets = [
            AutoComboboxWidget(lookup_class, allow_new=self.allow_new),
            forms.HiddenInput(attrs={u'data-selectable-type': 'hidden'})
        ]
        super(AutoComboboxSelectWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            lookup = self.lookup_class()
            item = lookup.get_item(value)
            item_value = lookup.get_item_value(item)
            return [item_value, value]
        return [None, None]


