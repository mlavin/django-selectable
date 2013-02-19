"""
Larger functional tests for fields and widgets.
"""
from __future__ import unicode_literals

from django import forms

from selectable.forms import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from selectable.forms import AutoCompleteSelectWidget, AutoComboboxSelectWidget
from selectable.tests import ManyThing, OtherThing, ThingLookup
from selectable.tests.base import BaseSelectableTestCase, parsed_inputs


__all__ = (
    'FuncAutoCompleteSelectTestCase',
    'FuncSelectModelChoiceTestCase',
    'FuncComboboxModelChoiceTestCase',
    'FuncManytoManyMultipleSelectTestCase',
    'FuncFormTestCase',
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
            'thing_1': '', # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), 'Form should not be valid')
        self.assertFalse('name' in form.errors)
        self.assertTrue('thing' in form.errors)

    def test_invalid_form_missing_name(self):
        "Invalid form using an AutoCompleteSelectField."
        data = {
            'name': '',
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), 'Form should not be valid')
        self.assertTrue('name' in form.errors)
        self.assertFalse('thing' in form.errors)

    def test_invalid_but_still_selected(self):
        "Invalid form should keep selected item."
        data = {
            'name': '',
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), 'Form should not be valid')
        rendered_form = form.as_p()
        inputs = parsed_inputs(rendered_form)
        # Selected text should be populated
        thing_0 = inputs['thing_0'][0]
        self.assertEqual(thing_0.attributes['value'].value, self.test_thing.name)
        # Selected pk should be populated
        thing_1 = inputs['thing_1'][0]
        self.assertEqual(int(thing_1.attributes['value'].value), self.test_thing.pk)

    def test_populate_from_model(self):
        "Populate from existing model."
        other_thing = OtherThing.objects.create(thing=self.test_thing, name='a')
        form = OtherThingForm(instance=other_thing)
        rendered_form = form.as_p()
        inputs = parsed_inputs(rendered_form)
        # Selected text should be populated
        thing_0 = inputs['thing_0'][0]
        self.assertEqual(thing_0.attributes['value'].value, self.test_thing.name)
        # Selected pk should be populated
        thing_1 = inputs['thing_1'][0]
        self.assertEqual(int(thing_1.attributes['value'].value), self.test_thing.pk)


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
        "Valid form using an AutoCompleteSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = SelectWidgetForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_missing_pk(self):
        "Invalid form (missing required pk) using an AutoCompleteSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': '', # Hidden input missing
        }
        form = SelectWidgetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('thing' in form.errors)

    def test_invalid_pk(self):
        "Invalid form (invalid pk value) using an AutoCompleteSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': 'XXX', # Hidden input doesn't match a PK
        }
        form = SelectWidgetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('thing' in form.errors)


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
        "Valid form using an AutoComboboxSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': self.test_thing.pk, # Hidden input
        }
        form = ComboboxSelectWidgetForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_missing_pk(self):
        "Invalid form (missing required pk) using an AutoComboboxSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': '', # Hidden input missing
        }
        form = SelectWidgetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('thing' in form.errors)

    def test_invalid_pk(self):
        "Invalid form (invalid pk value) using an AutoComboboxSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name, # Text input
            'thing_1': 'XXX', # Hidden input doesn't match a PK
        }
        form = SelectWidgetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('thing' in form.errors)


class ManyThingForm(forms.ModelForm):

    things = AutoCompleteSelectMultipleField(lookup_class=ThingLookup)

    class Meta(object):
        model = ManyThing


class FuncManytoManyMultipleSelectTestCase(BaseSelectableTestCase):
    """
    Functional tests for AutoCompleteSelectMultipleField compatibility
    with a ManyToManyField.
    """

    def setUp(self):
        self.test_thing = self.create_thing()

    def test_valid_form(self):
        "Valid form using an AutoCompleteSelectMultipleField."
        data = {
            'name': self.get_random_string(),
            'things_0': '', # Text input
            'things_1': [self.test_thing.pk, ], # Hidden inputs
        }
        form = ManyThingForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_valid_save(self):
        "Saving data from a valid form."
        data = {
            'name': self.get_random_string(),
            'things_0': '', # Text input
            'things_1': [self.test_thing.pk, ], # Hidden inputs
        }
        form = ManyThingForm(data=data)
        manything = form.save()
        self.assertEqual(manything.name, data['name'])
        things = manything.things.all()
        self.assertEqual(things.count(), 1)
        self.assertTrue(self.test_thing in things)

    def test_not_required(self):
        "Valid form where many to many is not required."
        data = {
            'name': self.get_random_string(),
            'things_0': '', # Text input
            'things_1': [], # Hidden inputs
        }
        form = ManyThingForm(data=data)
        form.fields['things'].required = False
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_not_required_save(self):
        "Saving data when many to many is not required."
        data = {
            'name': self.get_random_string(),
            'things_0': '', # Text input
            'things_1': [], # Hidden inputs
        }
        form = ManyThingForm(data=data)
        form.fields['things'].required = False
        manything = form.save()
        self.assertEqual(manything.name, data['name'])
        things = manything.things.all()
        self.assertEqual(things.count(), 0)

    def test_has_changed(self):
        "Populate intial data from a model."
        manything = ManyThing.objects.create(name='Foo')
        thing_1 = self.create_thing()
        manything.things.add(thing_1)
        data = {
            'name': manything.name,
            'things_0': '', # Text input
            'things_1': [thing_1.pk], # Hidden inputs
        }
        form = ManyThingForm(data=data, instance=manything)
        self.assertFalse(form.has_changed(), str(form.changed_data))


class SimpleForm(forms.Form):
    "Non-model form usage."
    thing = AutoCompleteSelectField(lookup_class=ThingLookup)
    new_thing = AutoCompleteSelectField(lookup_class=ThingLookup, allow_new=True)
    things = AutoCompleteSelectMultipleField(lookup_class=ThingLookup)


class FuncFormTestCase(BaseSelectableTestCase):
    """
    Functional tests for using AutoCompleteSelectField
    and AutoCompleteSelectMultipleField outside the context
    of a ModelForm.
    """

    def setUp(self):
        self.test_thing = self.create_thing()

    def test_blank_new_item(self):
        "Regression test for #91. new_thing is required but both are blank."
        data = {
            'thing_0': self.test_thing.name,
            'thing_1': self.test_thing.pk,
            'new_thing_0': '',
            'new_thing_1': '',
            'things_0': '',
            'things_1': [self.test_thing.pk, ]
        }
        form = SimpleForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('new_thing' in form.errors)

    def test_has_changed_with_empty_permitted(self):
        """
        Regression test for #92. has_changed fails when there is no initial and
        allow_new=False.
        """
        data = {
            'thing_0': '',
            'thing_1': self.test_thing.pk,
            'new_thing_0': self.test_thing.name,
            'new_thing_1': self.test_thing.pk,
            'things_0': '',
            'things_1': [self.test_thing.pk, ]
        }
        form = SimpleForm(data=data, empty_permitted=True)
        self.assertTrue(form.has_changed())
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_not_changed(self):
        """
        Regression test for #92. has_changed fails when there is no initial and
        allow_new=False.
        """
        data = {
            'thing_0': self.test_thing.name,
            'thing_1': self.test_thing.pk,
            'new_thing_0': self.test_thing.name,
            'new_thing_1': self.test_thing.pk,
            'things_0': '',
            'things_1': [self.test_thing.pk, ]
        }
        initial = {
            'thing': self.test_thing.pk,
            'new_thing': self.test_thing.pk,
            'things': [self.test_thing.pk, ]
        }
        form = SimpleForm(data=data, initial=initial)
        self.assertFalse(form.has_changed())
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_not_changed_with_empty_permitted(self):
        """
        Regression test for #92. has_changed fails when there is no initial and
        allow_new=False.
        """
        data = {
            'thing_0': '',
            'thing_1': '',
            'new_thing_0': '',
            'new_thing_1': '',
            'things_0': '',
            'things_1': '',
        }
        initial = {
            'thing': '',
            'new_thing': '',
            'things': '',
        }
        form = SimpleForm(data=data, initial=initial, empty_permitted=True)
        self.assertFalse(form.has_changed(), str(form.changed_data))
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_no_initial_with_empty_permitted(self):
        """
        If empty data is submitted and allowed with no initial then
        the form should not be seen as changed.
        """
        data = {
            'thing_0': '',
            'thing_1': '',
            'new_thing_0': '',
            'new_thing_1': '',
            'things_0': '',
            'things_1': '',
        }
        form = SimpleForm(data=data, empty_permitted=True)
        self.assertFalse(form.has_changed(), str(form.changed_data))
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_no_data_with_empty_permitted(self):
        """
        If no data is submitted and allowed with no initial then
        the form should not be seen as changed.
        """
        form = SimpleForm(data={}, empty_permitted=True)
        self.assertFalse(form.has_changed(), str(form.changed_data))
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_select_multiple_changed(self):
        """
        Detect changes for a multiple select input with and without
        initial data.
        """
        data = {
            'thing_0': '',
            'thing_1': '',
            'new_thing_0': '',
            'new_thing_1': '',
            'things_0': '',
            'things_1': [self.test_thing.pk, ]
        }
        form = SimpleForm(data=data)
        self.assertTrue(form.has_changed())
        self.assertTrue('things' in form.changed_data)

        initial = {
            'thing': '',
            'new_thing': '',
            'things': [self.test_thing.pk, ],
        }
        form = SimpleForm(data=data, initial=initial)
        self.assertFalse(form.has_changed(), str(form.changed_data))

        initial = {
            'thing': '',
            'new_thing': '',
            'things': [],
        }
        form = SimpleForm(data=data, initial=initial)
        self.assertTrue(form.has_changed())
        self.assertTrue('things' in form.changed_data)

    def test_single_select_changed(self):
        """
        Detect changes for a single select input with and without
        initial data.
        """
        data = {
            'thing_0': '',
            'thing_1': self.test_thing.pk,
            'new_thing_0': '',
            'new_thing_1': '',
            'things_0': '',
            'things_1': ''
        }
        form = SimpleForm(data=data)
        self.assertTrue(form.has_changed())
        self.assertTrue('thing' in form.changed_data)

        initial = {
            'thing': self.test_thing.pk,
            'new_thing': '',
            'things': '',
        }
        form = SimpleForm(data=data, initial=initial)
        self.assertFalse(form.has_changed(), str(form.changed_data))

        initial = {
            'thing': '',
            'new_thing': '',
            'things': '',
        }
        form = SimpleForm(data=data, initial=initial)
        self.assertTrue(form.has_changed())
        self.assertTrue('thing' in form.changed_data)

    def test_new_select_changed(self):
        """
        Detect changes for a single select input which allows new items
        with and without initial data.
        """
        data = {
            'thing_0': '',
            'thing_1': '',
            'new_thing_0': 'Foo',
            'new_thing_1': '',
            'things_0': '',
            'things_1': ''
        }
        form = SimpleForm(data=data)
        self.assertTrue(form.has_changed())
        self.assertTrue('new_thing' in form.changed_data)

        initial = {
            'thing': '',
            'new_thing': ['Foo', None],
            'things': '',
        }
        form = SimpleForm(data=data, initial=initial)
        self.assertFalse(form.has_changed(), str(form.changed_data))

        initial = {
            'thing': '',
            'new_thing': '',
            'things': '',
        }
        form = SimpleForm(data=data, initial=initial)
        self.assertTrue(form.has_changed())
        self.assertTrue('new_thing' in form.changed_data)