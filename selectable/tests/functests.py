"""
Larger functional tests for fields and widgets.
"""

from django import forms

from selectable.forms import AutoCompleteSelectField
from selectable.forms import AutoCompleteSelectWidget, AutoComboboxSelectWidget
from selectable.tests import OtherThing, ThingLookup
from selectable.tests.base import BaseSelectableTestCase


__all__ = (
    'FuncAutoCompleteSelectTestCase',
    'FuncSelectModelChoiceTestCase',
    'FuncComboboxModelChoiceTestCase',
)


class OtherThingForm(forms.ModelForm):

    thing = AutoCompleteSelectField(lookup_class=ThingLookup)

    class Meta(object):
        model = OtherThing


class FuncAutoCompleteSelectTestCase(BaseSelectableTestCase):

    def setUp(self):
        self.test_thing = self.create_thing()

    def test_valid_form(self):
        "Valid form using an AutoCompleteSelectField."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_invalid_form_missing_selected_pk(self):
        "Invalid form using an AutoCompleteSelectField."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': u'', # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), u'Form should not be valid')
        self.assertFalse('name' in form.errors)
        self.assertTrue('thing' in form.errors)

    def test_invalid_form_missing_name(self):
        "Invalid form using an AutoCompleteSelectField."
        data = {
            'name': u'',
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), u'Form should not be valid')
        self.assertTrue('name' in form.errors)
        self.assertFalse('thing' in form.errors)

    def test_invalid_but_still_selected(self):
        "Invalid form should keep selected item."
        data = {
            'name': u'',
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), u'Form should not be valid')
        rendered_form = form.as_p()
        # Selected text should be populated
        thing_0 = 'name="thing_0" value="%s"' % self.test_thing.name
        self.assertTrue(thing_0 in rendered_form, u"Didn't render selected text.")
        # Selected pk should be populated
        thing_1 = 'name="thing_1" value="%s"' % self.test_thing.pk
        self.assertTrue(thing_1 in rendered_form, u"Didn't render selected pk.")

    def test_populate_from_model(self):
        "Populate from existing model."
        other_thing = OtherThing.objects.create(thing=self.test_thing, name='a')
        form = OtherThingForm(instance=other_thing)
        rendered_form = form.as_p()
        # Selected text should be populated
        thing_0 = 'name="thing_0" value="%s"' % self.test_thing.name
        self.assertTrue(thing_0 in rendered_form, u"Didn't render selected text.")
        # Selected pk should be populated
        thing_1 = 'name="thing_1" value="%s"' % self.test_thing.pk
        self.assertTrue(thing_1 in rendered_form, u"Didn't render selected pk.")


class SelectWidgetForm(forms.ModelForm):

    class Meta(object):
        model = OtherThing
        widgets = {
            'thing': AutoCompleteSelectWidget(lookup_class=ThingLookup)
        }


class FuncSelectModelChoiceTestCase(BaseSelectableTestCase):
    """
    Functional tests for AutoCompleteSelectWidget compatibility
    with a ModelChoiceField.
    """

    def setUp(self):
        self.test_thing = self.create_thing()

    def test_valid_form(self):
        "Valid form using an AutoCompleteSelectField."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = SelectWidgetForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))


class ComboboxSelectWidgetForm(forms.ModelForm):

    class Meta(object):
        model = OtherThing
        widgets = {
            'thing': AutoComboboxSelectWidget(lookup_class=ThingLookup)
        }


class FuncComboboxModelChoiceTestCase(BaseSelectableTestCase):
    """
    Functional tests for AutoComboboxSelectWidget compatibility
    with a ModelChoiceField.
    """

    def setUp(self):
        self.test_thing = self.create_thing()

    def test_valid_form(self):
        "Valid form using an AutoCompleteSelectField."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = ComboboxSelectWidgetForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))
