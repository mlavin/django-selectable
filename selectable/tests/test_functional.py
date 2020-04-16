"""
Larger functional tests for fields and widgets.
"""
from django import forms

from ..forms import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from ..forms import AutoCompleteSelectWidget, AutoComboboxSelectWidget
from . import ManyThing, OtherThing, ThingLookup
from .base import BaseSelectableTestCase


__all__ = (
    'FuncAutoCompleteSelectTestCase',
    'FuncSelectModelChoiceTestCase',
    'FuncComboboxModelChoiceTestCase',
    'FuncManytoManyMultipleSelectTestCase',
    'FuncFormTestCase',
)


class OtherThingForm(forms.ModelForm):

    thing = AutoCompleteSelectField(lookup_class=ThingLookup)

    class Meta:
        model = OtherThing
        fields = ('name', 'thing', )


class FuncAutoCompleteSelectTestCase(BaseSelectableTestCase):

    def setUp(self):
        self.test_thing = self.create_thing()

    def test_valid_form(self):
        "Valid form using an AutoCompleteSelectField."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': self.test_thing.pk,  # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_invalid_form_missing_selected_pk(self):
        "Invalid form using an AutoCompleteSelectField."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': '',  # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), 'Form should not be valid')
        self.assertFalse('name' in form.errors)
        self.assertTrue('thing' in form.errors)

    def test_invalid_form_missing_name(self):
        "Invalid form using an AutoCompleteSelectField."
        data = {
            'name': '',
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': self.test_thing.pk,  # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), 'Form should not be valid')
        self.assertTrue('name' in form.errors)
        self.assertFalse('thing' in form.errors)

    def test_invalid_but_still_selected(self):
        "Invalid form should keep selected item."
        data = {
            'name': '',
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': self.test_thing.pk,  # Hidden input
        }
        form = OtherThingForm(data=data)
        self.assertFalse(form.is_valid(), 'Form should not be valid')
        rendered_form = form.as_p()
        # Selected text should be populated
        self.assertInHTML(
            '''
            <input data-selectable-allow-new="false" data-selectable-type="text"
                data-selectable-url="/selectable-tests/selectable-thinglookup/"
                id="id_thing_0" name="thing_0" type="text" value="{}" {} />
            '''.format(self.test_thing.name,
                       'required' if hasattr(form, 'use_required_attribute') else ''),
            rendered_form
        )
        # Selected pk should be populated
        self.assertInHTML(
            '''
            <input data-selectable-type="hidden" name="thing_1" id="id_thing_1"
                type="hidden" value="{}" {} />
            '''.format(self.test_thing.pk,
                       'required' if hasattr(form, 'use_required_attribute') else ''),
            rendered_form,
        )

    def test_populate_from_model(self):
        "Populate from existing model."
        other_thing = OtherThing.objects.create(thing=self.test_thing, name='a')
        form = OtherThingForm(instance=other_thing)
        rendered_form = form.as_p()
        # Selected text should be populated
        self.assertInHTML(
            '''
            <input data-selectable-allow-new="false" data-selectable-type="text"
                data-selectable-url="/selectable-tests/selectable-thinglookup/"
                id="id_thing_0" name="thing_0" type="text" value="{}" {} />
            '''.format(self.test_thing.name,
                       'required' if hasattr(form, 'use_required_attribute') else ''),
            rendered_form
        )
        # Selected pk should be populated
        self.assertInHTML(
            '''
            <input data-selectable-type="hidden" name="thing_1" id="id_thing_1"
                type="hidden" value="{}" {} />
            '''.format(self.test_thing.pk,
                       'required' if hasattr(form, 'use_required_attribute') else ''),
            rendered_form
        )


class SelectWidgetForm(forms.ModelForm):

    class Meta:
        model = OtherThing
        fields = ('name', 'thing', )
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
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': self.test_thing.pk,  # Hidden input
        }
        form = SelectWidgetForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_missing_pk(self):
        "Invalid form (missing required pk) using an AutoCompleteSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': '',  # Hidden input missing
        }
        form = SelectWidgetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('thing' in form.errors)

    def test_invalid_pk(self):
        "Invalid form (invalid pk value) using an AutoCompleteSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': 'XXX',  # Hidden input doesn't match a PK
        }
        form = SelectWidgetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('thing' in form.errors)

    def test_post_compatibility(self):
        """
        If new items are not allowed then the original field
        name can be included in the POST with the selected id.
        """
        data = {
            'name': self.get_random_string(),
            'thing': self.test_thing.pk,
        }
        form = SelectWidgetForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))


class ComboboxSelectWidgetForm(forms.ModelForm):

    class Meta:
        model = OtherThing
        fields = ('name', 'thing', )
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
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': self.test_thing.pk,  # Hidden input
        }
        form = ComboboxSelectWidgetForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_missing_pk(self):
        "Invalid form (missing required pk) using an AutoComboboxSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': '',  # Hidden input missing
        }
        form = ComboboxSelectWidgetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('thing' in form.errors)

    def test_invalid_pk(self):
        "Invalid form (invalid pk value) using an AutoComboboxSelectWidget."
        data = {
            'name': self.get_random_string(),
            'thing_0': self.test_thing.name,  # Text input
            'thing_1': 'XXX',  # Hidden input doesn't match a PK
        }
        form = ComboboxSelectWidgetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('thing' in form.errors)

    def test_post_compatibility(self):
        """
        If new items are not allowed then the original field
        name can be included in the POST with the selected id.
        """
        data = {
            'name': self.get_random_string(),
            'thing': self.test_thing.pk,
        }
        form = ComboboxSelectWidgetForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))


class ManyThingForm(forms.ModelForm):

    things = AutoCompleteSelectMultipleField(lookup_class=ThingLookup)

    class Meta:
        model = ManyThing
        fields = ('name', 'things', )


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
            'things_0': '',  # Text input
            'things_1': [self.test_thing.pk, ],  # Hidden inputs
        }
        form = ManyThingForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_valid_save(self):
        "Saving data from a valid form."
        data = {
            'name': self.get_random_string(),
            'things_0': '',  # Text input
            'things_1': [self.test_thing.pk, ],  # Hidden inputs
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
            'things_0': '',  # Text input
            'things_1': [],  # Hidden inputs
        }
        form = ManyThingForm(data=data)
        form.fields['things'].required = False
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_not_required_save(self):
        "Saving data when many to many is not required."
        data = {
            'name': self.get_random_string(),
            'things_0': '',  # Text input
            'things_1': [],  # Hidden inputs
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
            'things_0': '',  # Text input
            'things_1': [thing_1.pk],  # Hidden inputs
        }
        form = ManyThingForm(data=data, instance=manything)
        self.assertFalse(form.has_changed(), str(form.changed_data))

    def test_post_compatibility(self):
        """
        If new items are not allowed then the original field
        name can be included in the POST with the selected ids.
        """
        data = {
            'name': self.get_random_string(),
            'things': [self.test_thing.pk, ],
        }
        form = ManyThingForm(data=data)
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_render_form(self):
        thing_1 = self.create_thing()
        manything = ManyThing.objects.create(name='Foo')
        manything.things.add(thing_1)
        form = ManyThingForm(instance=manything)
        rendered = form.as_p()
        self.assertIn('title="{0}"'.format(thing_1.name),
                      rendered)


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
        form = SimpleForm(data=data, empty_permitted=True, use_required_attribute=False)
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
        form = SimpleForm(data=data, initial=initial, empty_permitted=True, use_required_attribute=False)
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
        form = SimpleForm(data=data, empty_permitted=True, use_required_attribute=False)
        self.assertFalse(form.has_changed(), str(form.changed_data))
        self.assertTrue(form.is_valid(), str(form.errors))

    def test_no_data_with_empty_permitted(self):
        """
        If no data is submitted and allowed with no initial then
        the form should not be seen as changed.
        """
        form = SimpleForm(data={}, empty_permitted=True, use_required_attribute=False)
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
