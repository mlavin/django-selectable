from django import forms
from django.utils import unittest

from selectable.forms import fields
from selectable.tests import Thing, ThingLookup
from selectable.tests.base import BaseSelectableTestCase
from selectable.tests.forms import Form1


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

    def test_initial(self):
        t1 = self.create_thing()
        f1 = Form1(initial={
            'f': Thing.objects.filter(
                pk=t1.pk
            ).values_list('pk', flat=True)})
        rendered_value = f1.as_p()
        hidden_widget_expected = 'value="%d" data-selectable-type="hidden-multiple" type="hidden"' % t1.pk
        c = rendered_value.count(hidden_widget_expected)
        ev = 1
        msg = c < ev and \
            'Did not find:\n\t%s\nas expected in:\n\t%s' % (hidden_widget_expected, rendered_value) or \
            'Found:\n\t%s\ntoo many times (%d) in:\n\t%s\nexpecting onnly %d' % (hidden_widget_expected, c, rendered_value, ev)
        self.assertEquals(c, ev, msg)

    def test_initial_multiple(self):
        t1 = self.create_thing()
        t2 = self.create_thing()
        f1 = Form1(initial={
            'f': Thing.objects.filter(
                pk__in=[t1.pk, t2.pk]
            ).values_list('pk', flat=True)})
        rendered_value = f1.as_p()
        ev = 1
        for t in [t1, t2]:
            hidden_widget_expected = 'value="%d" data-selectable-type="hidden-multiple" type="hidden"' % t.pk
            c = rendered_value.count(hidden_widget_expected)
            msg = c < ev and \
                'Did not find:\n\t%s\nas expected in:\n\t%s' % (hidden_widget_expected, rendered_value) or \
                'Found:\n\t%s\ntoo many times (%d) in:\n\t%s\nexpecting onnly %d' % (hidden_widget_expected, c, rendered_value, ev)
            self.assertEquals(c, ev, msg)

    @unittest.expectedFailure
    def test_initial_multiple_list(self):
        t1 = self.create_thing()
        t2 = self.create_thing()
        f1 = Form1(initial={
            'f': list(Thing.objects.filter(
                pk__in=[t1.pk, t2.pk]
            ).values_list('pk', flat=True))})
        rendered_value = f1.as_p()
        ev = 1
        for t in [t1, t2]:
            hidden_widget_expected = 'value="%d" data-selectable-type="hidden-multiple" type="hidden"' % t.pk
            c = rendered_value.count(hidden_widget_expected)
            msg = c < ev and \
                'Did not find:\n\t%s\nas expected in:\n\t%s' % (hidden_widget_expected, rendered_value) or \
                'Found:\n\t%s\ntoo many times (%d) in:\n\t%s\nexpecting onnly %d' % (hidden_widget_expected, c, rendered_value, ev)
            self.assertEquals(c, ev, msg)

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

