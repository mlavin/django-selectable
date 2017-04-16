from __future__ import unicode_literals

from django import forms, VERSION as DJANGO_VERSION
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _
from django.db.models import Model

from selectable.forms.base import import_lookup_class
from selectable.forms.widgets import AutoCompleteSelectWidget
from selectable.forms.widgets import AutoCompleteSelectMultipleWidget

__all__ = (
    'AutoCompleteSelectField',
    'AutoCompleteSelectMultipleField',
)


def model_vars(obj):
    fields = dict(
        (field.name, getattr(obj, field.name))
        for field in obj._meta.fields
    )
    return fields


class BaseAutoCompleteField(forms.Field):

    def has_changed(self, initial, data):
        "Detects if the data was changed. This is added in 1.6."
        if initial is None and data is None:
            return False
        if data and not hasattr(data, '__iter__'):
            data = self.widget.decompress(data)
        initial = self.to_python(initial)
        data = self.to_python(data)
        if hasattr(self, '_coerce'):
            data = self._coerce(data)
        if isinstance(data, Model) and isinstance(initial, Model):
            return model_vars(data) != model_vars(initial)
        else:
            return data != initial

    if DJANGO_VERSION < (1, 8):
        def _has_changed(self, initial, data):
            return self.has_changed(initial, data)


class AutoCompleteSelectField(BaseAutoCompleteField):
    widget = AutoCompleteSelectWidget

    default_error_messages = {
        'invalid_choice': _('Select a valid choice. That choice is not one of the available choices.'),
    }

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        widget = kwargs.get('widget', self.widget) or self.widget
        if isinstance(widget, type):
            kwargs['widget'] = widget(lookup_class, allow_new=self.allow_new, limit=self.limit)
        super(AutoCompleteSelectField, self).__init__(*args, **kwargs)



    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        lookup = self.lookup_class()
        if isinstance(value, list):
            # Input comes from an AutoComplete widget. It's two
            # components: text and id
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid_choice'])
            label, pk = value
            if pk in EMPTY_VALUES:
                if not self.allow_new:
                    if label:
                        raise ValidationError(self.error_messages['invalid_choice'])
                    else:
                        return None
                if label in EMPTY_VALUES:
                    return None
                try:
                    value = lookup.create_item(label)
                except ValueError:
                    raise ValidationError(self.error_messages['invalid_choice'])
            else:
                value = lookup.get_item(pk)
                if value is None:
                    raise ValidationError(self.error_messages['invalid_choice'])
        else:
            value = lookup.get_item(value)
            if value is None:
                raise ValidationError(self.error_messages['invalid_choice'])
        return value


class AutoCompleteSelectMultipleField(BaseAutoCompleteField):
    widget = AutoCompleteSelectMultipleWidget

    default_error_messages = {
        'invalid_choice': _('Select a valid choice. That choice is not one of the available choices.'),
    }

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = import_lookup_class(lookup_class)
        self.limit = kwargs.pop('limit', None)
        widget = kwargs.get('widget', self.widget) or self.widget
        if isinstance(widget, type):
            kwargs['widget'] = widget(lookup_class, limit=self.limit)
        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return []
        lookup = self.lookup_class()
        items = []
        for v in value:
            if v not in EMPTY_VALUES:
                item = lookup.get_item(v)
                if item is None:
                    raise ValidationError(self.error_messages['invalid_choice'])
                items.append(item)
        return items
