from django import forms

from selectable.forms import fields
from selectable.tests import ThingLookup
from selectable.tests.base import BaseSelectableTestCase


__all__ = (
    'AutoCompleteSelectFieldTestCase',
    'AutoComboboxSelectFieldTestCase',
    'AutoCompleteSelectMultipleFieldTestCase',
    'AutoComboboxSelectMultipleFieldTestCase',
)


class BaseFieldTestCase(BaseSelectableTestCase):
    field_cls = None
    lookup_cls = None

    def get_field_instance(self, allow_new=False):
        return self.__class__.field_cls(self.__class__.lookup_cls, allow_new=allow_new)

    def test_init(self):
        field = self.get_field_instance()
        self.assertEqual(field.lookup_class, self.__class__.lookup_cls)

    def test_clean(self):
        self.fail('This test has not yet been written')


class AutoCompleteSelectFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoCompleteSelectField
    lookup_cls = ThingLookup

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.name, thing.id])
        self.assertEqual(thing, value)

    def test_new_not_allowed(self):
        field = self.get_field_instance()
        value = self.get_random_string()
        self.assertRaises(forms.ValidationError, field.clean, [value, ''])

    def test_new_allowed(self):
        field = self.get_field_instance(allow_new=True)
        value = self.get_random_string()
        value = field.clean([value, ''])
        self.assertTrue(isinstance(value, ThingLookup.model))


class AutoComboboxSelectFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoComboboxSelectField
    lookup_cls = ThingLookup

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.name, thing.id])
        self.assertEqual(thing, value)

    def test_new_not_allowed(self):
        field = self.get_field_instance()
        value = self.get_random_string()
        self.assertRaises(forms.ValidationError, field.clean, [value, ''])

    def test_new_allowed(self):
        field = self.get_field_instance(allow_new=True)
        value = self.get_random_string()
        value = field.clean([value, ''])
        self.assertTrue(isinstance(value, ThingLookup.model))


class AutoCompleteSelectMultipleFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoCompleteSelectMultipleField
    lookup_cls = ThingLookup

    def get_field_instance(self):
        return self.__class__.field_cls(self.__class__.lookup_cls)

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.name, thing.id])
        self.assertEqual([thing], value)

    def test_clean_multiple(self):
        thing = self.create_thing()
        other_thing = self.create_thing()
        field = self.get_field_instance()
        names = [thing.name, other_thing.name]
        ids = [thing.id, other_thing.id]
        value = field.clean([names, ids])
        self.assertEqual([thing, other_thing], value)


class AutoComboboxSelectMultipleFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoComboboxSelectMultipleField
    lookup_cls = ThingLookup

    def get_field_instance(self):
        return self.__class__.field_cls(self.__class__.lookup_cls)

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.name, thing.id])
        self.assertEqual([thing], value)

    def test_clean_multiple(self):
        thing = self.create_thing()
        other_thing = self.create_thing()
        field = self.get_field_instance()
        names = [thing.name, other_thing.name]
        ids = [thing.id, other_thing.id]
        value = field.clean([names, ids])
        self.assertEqual([thing, other_thing], value)

