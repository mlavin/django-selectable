from django import forms

from selectable.forms import widgets
from selectable.tests import ThingLookup
from selectable.tests.base import BaseSelectableTestCase


__all__ = (
    'AutoCompleteWidgetTestCase',
    'AutoCompleteSelectWidgetTestCase',
    'AutoComboboxWidgetTestCase',
    'AutoComboboxSelectWidgetTestCase',
    'AutoCompleteSelectMultipleWidgetTestCase',
    'AutoComboboxSelectMultipleWidgetTestCase',
)


class BaseWidgetTestCase(BaseSelectableTestCase):
    widget_cls = None
    lookup_cls = None

    def get_widget_instance(self):
        return self.__class__.widget_cls(self.__class__.lookup_cls)

    def test_init(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.lookup_class, self.__class__.lookup_cls)


class AutoCompleteWidgetTestCase(BaseWidgetTestCase):
    widget_cls = widgets.AutoCompleteWidget
    lookup_cls = ThingLookup

    def test_build_attrs(self):
        widget = self.get_widget_instance()
        attrs = widget.build_attrs()
        self.assertTrue('data-selectable-url' in attrs)
        self.assertTrue('data-selectable-type' in attrs)
        self.assertTrue('data-selectable-allow-new' in attrs)


class AutoCompleteSelectWidgetTestCase(BaseWidgetTestCase):
    widget_cls = widgets.AutoCompleteSelectWidget
    lookup_cls = ThingLookup

    def test_has_complete_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[0].__class__, widgets.AutoCompleteWidget)

    def test_has_hidden_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[1].__class__, forms.HiddenInput)

    def test_hidden_type(self):
        widget = self.get_widget_instance()
        sub_widget = widget.widgets[1]
        attrs = sub_widget.build_attrs()
        self.assertTrue('data-selectable-type' in attrs)
        self.assertEqual(attrs['data-selectable-type'], 'hidden')


class AutoComboboxWidgetTestCase(BaseWidgetTestCase):
    widget_cls = widgets.AutoComboboxWidget
    lookup_cls = ThingLookup

    def test_build_attrs(self):
        widget = self.get_widget_instance()
        attrs = widget.build_attrs()
        self.assertTrue('data-selectable-url' in attrs)
        self.assertTrue('data-selectable-type' in attrs)
        self.assertTrue('data-selectable-allow-new' in attrs)


class AutoComboboxSelectWidgetTestCase(BaseWidgetTestCase):
    widget_cls = widgets.AutoComboboxSelectWidget
    lookup_cls = ThingLookup

    def test_has_complete_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[0].__class__, widgets.AutoComboboxWidget)

    def test_has_hidden_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[1].__class__, forms.HiddenInput)

    def test_hidden_type(self):
        widget = self.get_widget_instance()
        sub_widget = widget.widgets[1]
        attrs = sub_widget.build_attrs()
        self.assertTrue('data-selectable-type' in attrs)
        self.assertEqual(attrs['data-selectable-type'], 'hidden')


class AutoCompleteSelectMultipleWidgetTestCase(BaseWidgetTestCase):
    widget_cls = widgets.AutoCompleteSelectMultipleWidget
    lookup_cls = ThingLookup

    def test_has_complete_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[0].__class__, widgets.AutoCompleteWidget)

    def test_multiple_attr(self):
        widget = self.get_widget_instance()
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        self.assertTrue('data-selectable-multiple' in attrs)
        self.assertEqual(attrs['data-selectable-multiple'], 'true')

    def test_has_hidden_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[1].__class__, widgets.LookupMultipleHiddenInput)

    def test_hidden_type(self):
        widget = self.get_widget_instance()
        sub_widget = widget.widgets[1]
        attrs = sub_widget.build_attrs()
        self.assertTrue('data-selectable-type' in attrs)
        self.assertEqual(attrs['data-selectable-type'], 'hidden-multiple')


class AutoComboboxSelectMultipleWidgetTestCase(BaseWidgetTestCase):
    widget_cls = widgets.AutoComboboxSelectMultipleWidget
    lookup_cls = ThingLookup

    def test_has_complete_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[0].__class__, widgets.AutoComboboxWidget)

    def test_multiple_attr(self):
        widget = self.get_widget_instance()
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        self.assertTrue('data-selectable-multiple' in attrs)
        self.assertEqual(attrs['data-selectable-multiple'], 'true')

    def test_has_hidden_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[1].__class__, widgets.LookupMultipleHiddenInput)

    def test_hidden_type(self):
        widget = self.get_widget_instance()
        sub_widget = widget.widgets[1]
        attrs = sub_widget.build_attrs()
        self.assertTrue('data-selectable-type' in attrs)
        self.assertEqual(attrs['data-selectable-type'], 'hidden-multiple')

