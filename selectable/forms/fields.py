from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext as _

from selectable.forms.widgets import AutoCompleteSelectWidget, AutoComboboxSelectWidget
from selectable.forms.widgets import AutoCompleteSelectMultipleWidget, AutoComboboxSelectMultipleWidget

__all__ = (
    'AutoCompleteSelectField',
    'AutoComboboxSelectField',
    'AutoCompleteSelectMultipleField',
    'AutoComboboxSelectMultipleField',
)


class AutoCompleteSelectField(forms.Field):
    widget = AutoCompleteSelectWidget

    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of the available choices.'),
    }

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        kwargs['widget'] = self.widget(lookup_class, allow_new=self.allow_new, limit=self.limit)
        super(AutoCompleteSelectField, self).__init__(*args, **kwargs)


    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        lookup =self.lookup_class()
        if isinstance(value, list):
            # Input comes from an AutoComplete widget. It's two
            # components: text and id
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid_choice'])
            if value[1] in EMPTY_VALUES:
                if not self.allow_new:
                    if value[0]:
                        raise ValidationError(self.error_messages['invalid_choice'])
                    else:
                        return None
                value = lookup.create_item(value[0])  
            else:
                value = lookup.get_item(value[1])
                if value is None:
                    raise ValidationError(self.error_messages['invalid_choice'])
        else:
            value = lookup.get_item(value)
            if value is None:
                raise ValidationError(self.error_messages['invalid_choice'])
        return value


class AutoComboboxSelectField(AutoCompleteSelectField):
    widget = AutoComboboxSelectWidget


class AutoCompleteSelectMultipleField(forms.Field):
    widget = AutoCompleteSelectMultipleWidget

    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of the available choices.'),
    }

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.limit = kwargs.pop('limit', None)
        kwargs['widget'] = self.widget(lookup_class, limit=self.limit)
        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        lookup = self.lookup_class()
        items = []
        for v in value:
            if v not in EMPTY_VALUES:
                item = lookup.get_item(v)
                if item is None:
                    raise ValidationError(self.error_messages['invalid_choice'])
                items.append(item)
        return items


class AutoComboboxSelectMultipleField(AutoCompleteSelectMultipleField):
    widget = AutoComboboxSelectMultipleWidget

