from __future__ import unicode_literals

import json

from django import forms
from django.conf import settings
from django.forms.util import flatatt
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from selectable import __version__
from selectable.compat import force_text
from selectable.forms.base import import_lookup_class

__all__ = (
    'AutoCompleteWidget',
    'AutoCompleteSelectWidget',
    'AutoComboboxWidget',
    'AutoComboboxSelectWidget',
    'AutoCompleteSelectMultipleWidget',
    'AutoComboboxSelectMultipleWidget',
)


STATIC_PREFIX = '%sselectable/' % settings.STATIC_URL


class SelectableMediaMixin(object):

    class Media(object):
        css = {
            'all': ('%scss/dj.selectable.css?v=%s' % (STATIC_PREFIX, __version__),)
        }
        js = ('%sjs/jquery.dj.selectable.js?v=%s' % (STATIC_PREFIX, __version__),)

class AutoCompleteWidget(forms.TextInput, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        self.allow_new = kwargs.pop('allow_new', False)
        self.qs = kwargs.pop('query_params', {})
        self.limit = kwargs.pop('limit', None)
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def update_query_parameters(self, qs_dict):
        self.qs.update(qs_dict)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutoCompleteWidget, self).build_attrs(extra_attrs, **kwargs)
        url = self.lookup_class.url()
        if self.limit and 'limit' not in self.qs:
            self.qs['limit'] = self.limit
        if self.qs:
            url = '%s?%s' % (url, urlencode(self.qs))
        if 'data-selectable-options' in attrs:
            attrs['data-selectable-options'] = json.dumps(attrs['data-selectable-options'])
        attrs['data-selectable-url'] = url
        attrs['data-selectable-type'] = 'text'
        attrs['data-selectable-allow-new'] = str(self.allow_new).lower()
        return attrs


class SelectableMultiWidget(forms.MultiWidget):

    def update_query_parameters(self, qs_dict):
        self.widgets[0].update_query_parameters(qs_dict)

    def _has_changed(self, initial, data):
        "Decects if the widget was changed. This is removed in 1.6."
        if initial is None and data is None:
            return False
        if data and not hasattr(data, '__iter__'):
            data = self.decompress(data)
        return super(SelectableMultiWidget, self)._has_changed(initial, data)

    def decompress(self, value):
        if value:
            lookup = self.lookup_class()
            model = getattr(self.lookup_class, 'model', None)
            if model and isinstance(value, model):
                item = value
                value = lookup.get_item_id(item)
            else:
                item = lookup.get_item(value)
            item_value = lookup.get_item_value(item)
            return [item_value, value]
        return [None, None]


class AutoCompleteSelectWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        query_params = kwargs.pop('query_params', {})
        widgets = [
            AutoCompleteWidget(
                lookup_class, allow_new=self.allow_new,
                limit=self.limit, query_params=query_params,
                attrs=kwargs.get('attrs'),
            ),
            forms.HiddenInput(attrs={'data-selectable-type': 'hidden'})
        ]
        super(AutoCompleteSelectWidget, self).__init__(widgets, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        value = super(AutoCompleteSelectWidget, self).value_from_datadict(data, files, name)
        if not self.allow_new:
            return value[1]
        return value


class AutoComboboxWidget(AutoCompleteWidget, SelectableMediaMixin):

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutoComboboxWidget, self).build_attrs(extra_attrs, **kwargs)
        attrs['data-selectable-type'] = 'combobox'
        return attrs


class AutoComboboxSelectWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        query_params = kwargs.pop('query_params', {})
        widgets = [
            AutoComboboxWidget(
                lookup_class, allow_new=self.allow_new,
                limit=self.limit, query_params=query_params,
                attrs=kwargs.get('attrs'),
            ),
            forms.HiddenInput(attrs={'data-selectable-type': 'hidden'})
        ]
        super(AutoComboboxSelectWidget, self).__init__(widgets, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        value = super(AutoComboboxSelectWidget, self).value_from_datadict(data, files, name)
        if not self.allow_new:
            return value[1]
        return value


class LookupMultipleHiddenInput(forms.MultipleHiddenInput):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        super(LookupMultipleHiddenInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        lookup = self.lookup_class()
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        inputs = []
        model = getattr(self.lookup_class, 'model', None)
        for i, v in enumerate(value):
            item = None
            if model and isinstance(v, model):
                item = v
                v = lookup.get_item_id(item)
            input_attrs = dict(value=force_text(v), **final_attrs)
            if id_:
                # An ID attribute was given. Add a numeric index as a suffix
                # so that the inputs don't all have the same ID attribute.
                input_attrs['id'] = '%s_%s' % (id_, i)
            if v:
                item = item or lookup.get_item(v)
                input_attrs['title'] = lookup.get_item_value(item)
            inputs.append('<input%s />' % flatatt(input_attrs))
        return mark_safe('\n'.join(inputs))

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(LookupMultipleHiddenInput, self).build_attrs(extra_attrs, **kwargs)
        attrs['data-selectable-type'] = 'hidden-multiple'
        return attrs


class AutoCompleteSelectMultipleWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        self.limit = kwargs.pop('limit', None)
        position = kwargs.pop('position', 'bottom')
        attrs = {
            'data-selectable-multiple': 'true',
            'data-selectable-position': position
        }
        attrs.update(kwargs.get('attrs', {}))
        query_params = kwargs.pop('query_params', {})
        widgets = [
            AutoCompleteWidget(
                lookup_class, allow_new=False,
                limit=self.limit, query_params=query_params, attrs=attrs
            ),
            LookupMultipleHiddenInput(lookup_class)
        ]
        super(AutoCompleteSelectMultipleWidget, self).__init__(widgets, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return self.widgets[1].value_from_datadict(data, files, name + '_1')

    def render(self, name, value, attrs=None):
        if value and not hasattr(value, '__iter__'):
            value = [value]
        value = ['', value]
        return super(AutoCompleteSelectMultipleWidget, self).render(name, value, attrs)

    def _has_changed(self, initial, data):
        """"
        Decects if the widget was changed. This is removed in 1.6.

        For the multi-select case we only care if the hidden inputs changed.
        """
        initial = ['', initial]
        data = ['', data]
        return super(AutoCompleteSelectMultipleWidget, self)._has_changed(initial, data)



class AutoComboboxSelectMultipleWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        self.limit = kwargs.pop('limit', None)
        position = kwargs.pop('position', 'bottom')
        attrs = {
            'data-selectable-multiple': 'true',
            'data-selectable-position': position
        }
        attrs.update(kwargs.get('attrs', {}))
        query_params = kwargs.pop('query_params', {})
        widgets = [
            AutoComboboxWidget(
                lookup_class, allow_new=False,
                limit=self.limit, query_params=query_params, attrs=attrs
            ),
            LookupMultipleHiddenInput(lookup_class)
        ]
        super(AutoComboboxSelectMultipleWidget, self).__init__(widgets, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return self.widgets[1].value_from_datadict(data, files, name + '_1')

    def render(self, name, value, attrs=None):
        if value and not hasattr(value, '__iter__'):
            value = [value]
        value = ['', value]
        return super(AutoComboboxSelectMultipleWidget, self).render(name, value, attrs)

    def _has_changed(self, initial, data):
        """"
        Decects if the widget was changed. This is removed in 1.6.

        For the multi-select case we only care if the hidden inputs changed.
        """
        initial = ['', initial]
        data = ['', data]
        return super(AutoComboboxSelectMultipleWidget, self)._has_changed(initial, data)
