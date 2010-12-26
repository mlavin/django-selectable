from django import forms
from django.conf import settings
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


__all__ = (
    'AutoCompleteWidget',
    'AutoCompleteSelectWidget',
    'AutoComboboxWidget',
    'AutoComboboxSelectWidget',
    'AutoCompleteSelectMultipleWidget',
    'AutoComboboxSelectMultipleWidget',
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


class LookupMultipleHiddenInput(forms.MultipleHiddenInput):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        super(LookupMultipleHiddenInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        lookup = self.lookup_class()
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        inputs = []
        for i, v in enumerate(value):
            input_attrs = dict(value=force_unicode(v), **final_attrs)
            if id_:
                # An ID attribute was given. Add a numeric index as a suffix
                # so that the inputs don't all have the same ID attribute.
                input_attrs['id'] = '%s_%s' % (id_, i)
            if v:
                item = lookup.get_item(v)
                input_attrs['title'] = lookup.get_item_value(item)
            inputs.append(u'<input%s />' % flatatt(input_attrs))
        return mark_safe(u'\n'.join(inputs))

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(LookupMultipleHiddenInput, self).build_attrs(extra_attrs, **kwargs)
        attrs[u'data-selectable-type'] = 'hidden-multiple'
        return attrs


class AutoCompleteSelectMultipleWidget(forms.MultiWidget):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        widgets = [
            AutoCompleteWidget(lookup_class, allow_new=False, attrs={u'data-selectable-multiple': 'true'}),
            LookupMultipleHiddenInput(lookup_class)
        ]
        super(AutoCompleteSelectMultipleWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            if not isinstance(value, list):
                value = [value]
            return [None, value]
        return [None, None]


class AutoComboboxSelectMultipleWidget(forms.MultiWidget):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        widgets = [
            AutoComboboxWidget(lookup_class, allow_new=False, attrs={u'data-selectable-multiple': 'true'}),
            LookupMultipleHiddenInput(lookup_class)
        ]
        super(AutoComboboxSelectMultipleWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            if not isinstance(value, list):
                value = [value]
            return [None, value]
        return [None, None]

