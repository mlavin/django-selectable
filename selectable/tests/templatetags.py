from django.template import Template, Context

from selectable.tests.base import BaseSelectableTestCase

__all__ = (
    'JqueryTagTestCase',
    'ThemeTagTestCase',
)


class JqueryTagTestCase(BaseSelectableTestCase):

    def assertJQueryVersion(self, result, version):
        expected = "//ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js" % version
        self.assertTrue(expected in result)

    def assertUIVersion(self, result, version):
        expected = "//ajax.googleapis.com/ajax/libs/jqueryui/%s/jquery-ui.js" % version
        self.assertTrue(expected in result)

    def test_render(self):
        "Render template tag with default versions."
        template = Template("{% load selectable_tags %}{% include_jquery_libs %}")
        context = Context({})
        result = template.render(context)
        self.assertJQueryVersion(result, '1.7.2')
        self.assertUIVersion(result, '1.8.23')

    def test_render_jquery_version(self):
        "Render template tag with specified jQuery version."
        template = Template("{% load selectable_tags %}{% include_jquery_libs '1.4.3' %}")
        context = Context({})
        result = template.render(context)
        self.assertJQueryVersion(result, '1.4.3')

    def test_render_variable_jquery_version(self):
        "Render using jQuery version from the template context."
        version = '1.4.3'
        template = Template("{% load selectable_tags %}{% include_jquery_libs version %}")
        context = Context({'version': version})
        result = template.render(context)
        self.assertJQueryVersion(result, '1.4.3')

    def test_render_jquery_ui_version(self):
        "Render template tag with specified jQuery UI version."
        template = Template("{% load selectable_tags %}{% include_jquery_libs '1.4.3' '1.8.13' %}")
        context = Context({})
        result = template.render(context)
        self.assertUIVersion(result, '1.8.13')

    def test_render_variable_jquery_ui_version(self):
        "Render using jQuery UI version from the template context."
        version = '1.8.13'
        template = Template("{% load selectable_tags %}{% include_jquery_libs '1.4.3' version %}")
        context = Context({'version': version})
        result = template.render(context)
        self.assertUIVersion(result, '1.8.13')

    def test_render_no_jquery(self):
        "Render template tag without jQuery."
        template = Template("{% load selectable_tags %}{% include_jquery_libs '' %}")
        context = Context({})
        result = template.render(context)
        self.assertTrue('jquery.min.js' not in result)

    def test_render_no_jquery_ui(self):
        "Render template tag without jQuery UI."
        template = Template("{% load selectable_tags %}{% include_jquery_libs '1.7.2' '' %}")
        context = Context({})
        result = template.render(context)
        self.assertTrue('jquery-ui.js' not in result)


class ThemeTagTestCase(BaseSelectableTestCase):

    def assertUICSS(self, result, theme, version):
        expected = "//ajax.googleapis.com/ajax/libs/jqueryui/%s/themes/%s/jquery-ui.css" % (version, theme)
        self.assertTrue(expected in result)

    def test_render(self):
        "Render template tag with default settings."
        template = Template("{% load selectable_tags %}{% include_ui_theme %}")
        context = Context({})
        result = template.render(context)
        self.assertUICSS(result, 'base', '1.8.23')

    def test_render_version(self):
        "Render template tag with alternate version."
        template = Template("{% load selectable_tags %}{% include_ui_theme 'base' '1.8.13' %}")
        context = Context({})
        result = template.render(context)
        self.assertUICSS(result, 'base', '1.8.13')
        
    def test_variable_version(self):
        "Render using version from content variable."
        version = '1.8.13'
        template = Template("{% load selectable_tags %}{% include_ui_theme 'base' version %}")
        context = Context({'version': version})
        result = template.render(context)
        self.assertUICSS(result, 'base', version)

    def test_render_theme(self):
        "Render template tag with alternate theme."
        template = Template("{% load selectable_tags %}{% include_ui_theme 'ui-lightness' %}")
        context = Context({})
        result = template.render(context)
        self.assertUICSS(result, 'ui-lightness', '1.8.23')
        
    def test_variable_theme(self):
        "Render using theme from content variable."
        theme = 'ui-lightness'
        template = Template("{% load selectable_tags %}{% include_ui_theme theme %}")
        context = Context({'theme': theme})
        result = template.render(context)
        self.assertUICSS(result, theme, '1.8.23')
