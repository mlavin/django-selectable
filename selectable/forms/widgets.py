import json

from django import forms
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlencode

from selectable import __version__
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


class SelectableMediaMixin():

    class Media():
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
        super().__init__(*args, **kwargs)

    def update_query_parameters(self, qs_dict):
        self.qs.update(qs_dict)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
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

    def get_compatible_postdata(self, data, name):
        """Get postdata built for a normal <select> element.

        Django MultiWidgets create post variables like ``foo_0`` and ``foo_1``,
        and this behavior is not cleanly overridable.  Non-multiwidgets, like
        Select, get simple names like ``foo``. In order to keep this widget
        compatible with requests designed for traditional select widgets,
        search postdata for a name like ``foo`` and return that value.

        This will return ``None`` if a ``<select>``-compatibile post variable
        is not found.
        """
        return data.get(name, None)


class _BaseSingleSelectWidget(SelectableMultiWidget, SelectableMediaMixin):
    """
    Common base class for AutoCompleteSelectWidget and AutoComboboxSelectWidget
    each which use one widget (primary_widget) to select text and a single
    hidden input to hold the selected id.
    """

    primary_widget = None

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        query_params = kwargs.pop('query_params', {})
        widgets = [
            self.primary_widget(
                lookup_class, allow_new=self.allow_new,
                limit=self.limit, query_params=query_params,
                attrs=kwargs.get('attrs'),
            ),
            forms.HiddenInput(attrs={'data-selectable-type': 'hidden'})
        ]
        super().__init__(widgets, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if not value[1]:
            compatible_postdata = self.get_compatible_postdata(data, name)
            if compatible_postdata:
                value[1] = compatible_postdata
        if not self.allow_new:
            return value[1]
        return value


class AutoCompleteSelectWidget(_BaseSingleSelectWidget):

    primary_widget = AutoCompleteWidget


class AutoComboboxWidget(AutoCompleteWidget, SelectableMediaMixin):

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-selectable-type'] = 'combobox'
        return attrs


class AutoComboboxSelectWidget(_BaseSingleSelectWidget):

    primary_widget = AutoComboboxWidget


class LookupMultipleHiddenInput(forms.MultipleHiddenInput):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        lookup = self.lookup_class()
        values = self._normalize_value(value)
        values = list(values)  # force evaluation

        context = super().get_context(name, values, attrs)

        # Now override/add to what super() did:
        subwidgets = context['widget']['subwidgets']
        for widget_ctx, item in zip(subwidgets, values):
            input_value, title = self._lookup_value_and_title(lookup, item)
            widget_ctx['value'] = input_value  # override what super() did
            if title:
                widget_ctx['attrs']['title'] = title
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-selectable-type'] = 'hidden-multiple'
        return attrs

    def _normalize_value(self, value):
        if value is None:
            value = []
        return value

    def _lookup_value_and_title(self, lookup, v):
        model = getattr(self.lookup_class, 'model', None)
        item = None
        if model and isinstance(v, model):
            item = v
            v = lookup.get_item_id(item)
        title = None
        if v:
            item = item or lookup.get_item(v)
            title = lookup.get_item_value(item)
        return force_str(v), title


class _BaseMultipleSelectWidget(SelectableMultiWidget, SelectableMediaMixin):
    """
    Common base class for AutoCompleteSelectMultipleWidget and AutoComboboxSelectMultipleWidget
    each which use one widget (primary_widget) to select text and a multiple
    hidden inputs to hold the selected ids.
    """

    primary_widget = None

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
            self.primary_widget(
                lookup_class, allow_new=False,
                limit=self.limit, query_params=query_params, attrs=attrs
            ),
            LookupMultipleHiddenInput(lookup_class)
        ]
        super().__init__(widgets, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        value = self.widgets[1].value_from_datadict(data, files, name + '_1')
        if not value:
            # Fall back to the compatible POST name
            value = self.get_compatible_postdata(data, name)
        return value

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        if 'required' in attrs:
            attrs.pop('required')
        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        if value and not hasattr(value, '__iter__'):
            value = [value]
        value = ['', value]
        return super().render(name, value, attrs, renderer)


class AutoCompleteSelectMultipleWidget(_BaseMultipleSelectWidget):

    primary_widget = AutoCompleteWidget


class AutoComboboxSelectMultipleWidget(_BaseMultipleSelectWidget):

    primary_widget = AutoComboboxWidget
