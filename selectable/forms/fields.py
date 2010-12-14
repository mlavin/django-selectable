from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext as _

from selectable.forms.widgets import AutoCompleteSelectWidget, AutoComboboxSelectWidget

__all__ = (
    'AutoCompleteSelectField',
    'AutoComboboxSelectField',
)


class AutoCompleteSelectField(forms.Field):
    widget = AutoCompleteSelectWidget

    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of the available choices.'),
    }

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        kwargs['widget'] = self.widget(lookup_class, allow_new=self.allow_new)
        super(AutoCompleteSelectField, self).__init__(*args, **kwargs)


    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        if isinstance(value, list):
            # Input comes from a AutoCompleteSelectWidget. It's two
            # components: text and id
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid_choice'])
            lookup =self.lookup_class()
            if value[1] in EMPTY_VALUES:
                if not self.allow_new:
                    if value[0]:
                        raise ValidationError(self.error_messages['invalid_choice'])
                    else:
                        raise ValidationError(self.error_messages['required'])
                value = lookup.create_item(value[0])  
            else:
                value = lookup.get_item(value[1])
                if value is None:
                    raise ValidationError(self.error_messages['invalid_choice'])
        return value

class AutoComboboxSelectField(AutoCompleteSelectField):
    widget = AutoComboboxSelectWidget

