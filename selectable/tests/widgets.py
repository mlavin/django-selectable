from urlparse import urlparse

from django import forms
from django.utils.http import urlencode

from selectable.forms import widgets
from selectable.tests import Thing, ThingLookup
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

    def get_widget_instance(self, **kwargs):
        return self.__class__.widget_cls(self.__class__.lookup_cls, **kwargs)

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

    def test_update_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        attrs = widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))
        
    def test_limit_paramter(self):
        widget = self.get_widget_instance(limit=10)
        attrs = widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance(query_params=params)
        attrs = widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))


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

    def test_update_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_paramter(self):
        widget = self.get_widget_instance(limit=10)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance(query_params=params)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))


class AutoComboboxWidgetTestCase(BaseWidgetTestCase):
    widget_cls = widgets.AutoComboboxWidget
    lookup_cls = ThingLookup

    def test_build_attrs(self):
        widget = self.get_widget_instance()
        attrs = widget.build_attrs()
        self.assertTrue('data-selectable-url' in attrs)
        self.assertTrue('data-selectable-type' in attrs)
        self.assertTrue('data-selectable-allow-new' in attrs)

    def test_update_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        attrs = widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_paramter(self):
        widget = self.get_widget_instance(limit=10)
        attrs = widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance(query_params=params)
        attrs = widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))


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

    def test_update_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_paramter(self):
        widget = self.get_widget_instance(limit=10)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance(query_params=params)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))


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

    def test_render_single(self):
        widget = self.get_widget_instance()
        val = 4
        rendered_value = widget.render('field_name', val)
        ev = 'data-selectable-type="hidden-multiple" type="hidden" name="field_name_1" value="%d"' % val
        self.assertTrue(ev in rendered_value,
            "Did not find:\n\t%s\nin rendered value:\n\t%s" % (ev, rendered_value))

    def test_render_list(self):
        widget = self.get_widget_instance()
        list_val = [8, 5]
        rendered_value = widget.render('field_name', list_val)
        for v in list_val:
            ev = 'data-selectable-type="hidden-multiple" type="hidden" name="field_name_1" value="%d"' % v
            self.assertTrue(ev in rendered_value,
                "Did not find:\n\t%s\nin rendered value:\n\t%s" % (ev, rendered_value))

    def test_render_qs(self):
        widget = self.get_widget_instance()
        t1 = self.create_thing()
        t2 = self.create_thing()
        qs_val = Thing.objects.filter(pk__in=[t1.pk, t2.pk]).values_list('pk', flat=True)
        rendered_value = widget.render('field_name', qs_val)
        for t in qs_val:
            ev = 'data-selectable-type="hidden-multiple" type="hidden" name="field_name_1" value="%d"' % t
            self.assertTrue(ev in rendered_value,
                "Did not find:\n\t%s\nin rendered value:\n\t%s" % (ev, rendered_value))

    def test_update_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_paramter(self):
        widget = self.get_widget_instance(limit=10)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance(query_params=params)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))


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

    def test_render_single(self):
        widget = self.get_widget_instance()
        val = 4
        rendered_value = widget.render('field_name', val)
        ev = 'data-selectable-type="hidden-multiple" type="hidden" name="field_name_1" value="%d"' % val
        self.assertTrue(ev in rendered_value,
            "Did not find:\n\t%s\nin rendered value:\n\t%s" % (ev, rendered_value))

    def test_render_list(self):
        widget = self.get_widget_instance()
        list_val = [8, 5]
        rendered_value = widget.render('field_name', list_val)
        for v in list_val:
            ev = 'data-selectable-type="hidden-multiple" type="hidden" name="field_name_1" value="%d"' % v
            self.assertTrue(ev in rendered_value,
                "Did not find:\n\t%s\nin rendered value:\n\t%s" % (ev, rendered_value))

    def test_render_qs(self):
        widget = self.get_widget_instance()
        t1 = self.create_thing()
        t2 = self.create_thing()
        qs_val = Thing.objects.filter(pk__in=[t1.pk, t2.pk]).values_list('pk', flat=True)
        rendered_value = widget.render('field_name', qs_val)
        for t in qs_val:
            ev = 'data-selectable-type="hidden-multiple" type="hidden" name="field_name_1" value="%d"' % t
            self.assertTrue(ev in rendered_value,
                "Did not find:\n\t%s\nin rendered value:\n\t%s" % (ev, rendered_value))

    def test_update_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_paramter(self):
        widget = self.get_widget_instance(limit=10)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1} 
        widget = self.get_widget_instance(query_params=params)
        sub_widget = widget.widgets[0]
        attrs = sub_widget.build_attrs()
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

