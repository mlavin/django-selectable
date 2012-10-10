from django import forms

from selectable.forms import fields, widgets
from selectable.tests import ThingLookup
from selectable.tests.base import BaseSelectableTestCase


__all__ = (
    'AutoCompleteSelectFieldTestCase',
    'AutoCompleteSelectMultipleFieldTestCase',
)


class BaseFieldTestCase(BaseSelectableTestCase):
    field_cls = None
    lookup_cls = None

    def get_field_instance(self, allow_new=False, limit=None, widget=None):
        return self.field_cls(self.lookup_cls, allow_new=allow_new, limit=limit, widget=widget)

    def test_init(self):
        field = self.get_field_instance()
        self.assertEqual(field.lookup_class, self.lookup_cls)

    def test_init_with_limit(self):
        field = self.get_field_instance(limit=10)
        self.assertEqual(field.limit, 10)
        self.assertEqual(field.widget.limit, 10)

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

    def test_default_widget(self):
        field = self.get_field_instance()
        self.assertTrue(isinstance(field.widget, widgets.AutoCompleteSelectWidget))

    def test_alternate_widget(self):
        widget_cls = widgets.AutoComboboxWidget
        field = self.get_field_instance(widget=widget_cls)
        self.assertTrue(isinstance(field.widget, widget_cls))

    def test_alternate_widget_instance(self):
        widget = widgets.AutoComboboxWidget(self.lookup_cls)
        field = self.get_field_instance(widget=widget)
        self.assertTrue(isinstance(field.widget, widgets.AutoComboboxWidget))


class AutoCompleteSelectMultipleFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoCompleteSelectMultipleField
    lookup_cls = ThingLookup

    def get_field_instance(self, limit=None, widget=None):
        return self.field_cls(self.lookup_cls, limit=limit, widget=widget)

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.id])
        self.assertEqual([thing], value)

    def test_clean_multiple(self):
        thing = self.create_thing()
        other_thing = self.create_thing()
        field = self.get_field_instance()
        ids = [thing.id, other_thing.id]
        value = field.clean(ids)
        self.assertEqual([thing, other_thing], value)

    def test_default_widget(self):
        field = self.get_field_instance()
        self.assertTrue(isinstance(field.widget, widgets.AutoCompleteSelectMultipleWidget))

    def test_alternate_widget(self):
        widget_cls = widgets.AutoComboboxSelectMultipleWidget
        field = self.get_field_instance(widget=widget_cls)
        self.assertTrue(isinstance(field.widget, widget_cls))

    def test_alternate_widget_instance(self):
        widget = widgets.AutoComboboxSelectMultipleWidget(self.lookup_cls)
        field = self.get_field_instance(widget=widget)
        self.assertTrue(isinstance(field.widget, widgets.AutoComboboxSelectMultipleWidget))
