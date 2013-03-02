Testing Forms and Lookups
====================================

django-selectable has its own test suite for testing the rendering, validation
and server-side logic it provides. However, depending on the additional customizations
you add to your forms and lookups you most likely will want to include tests of your
own. This section contains some tips or techniques for testing your lookups.

This guide assumes that you are reasonable familiar with the concepts of unit testing
including Python's `unittest <http://docs.python.org/2/library/unittest.html>`_ module and
Django's `testing guide <https://docs.djangoproject.com/en/1.4/topics/testing/>`_.


Testing Forms with django-selectable
--------------------------------------------------

For the most part testing forms which use django-selectable's custom fields
and widgets is the same as testing any Django form. One point that is slightly
different is that the select and multi-select widgets are
`MultiWidgets <https://docs.djangoproject.com/en/1.4/ref/forms/widgets/#django.forms.MultiWidget>`_.
The effect of this is that there are two names in the post rather than one. Take the below
form for example.

    .. code-block:: python

        # models.py

        from django.db import models

        class Thing(models.Model):
            name = models.CharField(max_length=100)
            description = models.CharField(max_length=100)

            def __unicode__(self):
                return self.name

    .. code-block:: python

        # lookups.py

        from selectable.base import ModelLookup
        from selectable.registry import registry

        from .models import Thing

        class ThingLookup(ModelLookup):
            model = Thing
            search_fields = ('name__icontains', )

        registry.register(ThingLookup)

    .. code-block:: python

        # forms.py

        from django import forms

        from selectable.forms import AutoCompleteSelectField

        from .lookups import ThingLookup

        class SimpleForm(forms.Form):
            "Basic form for testing."
            thing = AutoCompleteSelectField(lookup_class=ThingLookup)

This form has a single field to select a ``Thing``. It does not allow
new items. Let's write some simple tests for this form.

    .. code-block:: python

        # tests.py

        from django.test import TestCase

        from .forms import SimpleForm
        from .models import Thing

        class SimpleFormTestCase(TestCase):

            def test_valid_form(self):
                "Submit valid data."
                thing = Thing.objects.create(name='Foo', description='Bar')
                data = {
                    'thing_0': thing.name,
                    'thing_1': thing.pk,
                }
                form = SimpleForm(data=data)
                self.assertTrue(form.is_valid())

            def test_invalid_form(self):
                "Thing is required but missing."
                data = {
                    'thing_0': 'Foo',
                    'thing_1': '',
                }
                form = SimpleForm(data=data)
                self.assertFalse(form.is_valid())

Here you will note that while there is only one field ``thing`` it requires
two items in the POST the first is for the text input and the second is for
the hidden input. This is again due to the use of MultiWidget for the selection.


Testing Lookup Results
--------------------------------------------------

Testing the lookups used by django-selectable is similar to testing your Django views.
While it might be tempting to use the Django
`test client <https://docs.djangoproject.com/en/1.4/topics/testing/#module-django.test.client>`_,
it is slightly easier to use the
`request factory <https://docs.djangoproject.com/en/1.4/topics/testing/#the-request-factory>`_.
A simple example is given below.

    .. code-block:: python

        # tests.py

        import json

        from django.test import TestCase
        from django.test.client import RequestFactory

        from .lookups import ThingLookup
        from .models import Thing

        class ThingLookupTestCase(TestCase):

            def setUp(self):
                self.factory = RequestFactory()
                self.lookup = ThingLookup()
                self.test_thing = Thing.objects.create(name='Foo', description='Bar')

            def test_results(self):
                "Test full response."
                request = self.factory.get("/", {'term': 'Fo'})
                response = self.lookup.results(request)
                data = json.loads(response.content)['data']
                self.assertEqual(1, len(data))
                self.assertEqual(self.test_thing.pk, data[1]['id'])

            def test_label(self):
                "Test item label."
                label = self.lookup.get_item_label(self.test_thing)
                self.assertEqual(self.test_thing.name, label)

As shown in the ``test_label`` example it is not required to test the full
request/response. You can test each of the methods in the lookup API individually.
When testing your lookups you should focus on testing the portions which have been
customized by your application.