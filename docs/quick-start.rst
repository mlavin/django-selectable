Getting Started
==================

The workflow for using `django-selectable` involves two main parts:
    - Defining your lookups
    - Defining your forms

This guide assumes that you have a basic knowledge of creating Django models and
forms. If not you should first read through the documentation on
`defining models <http://docs.djangoproject.com/en/1.3/topics/db/models/>`_
and `using forms <http://docs.djangoproject.com/en/1.3/topics/forms/>`_.

.. _start-include-jquery:

Including jQuery & jQuery UI
--------------------------------------

The widgets in django-selectable define the media they need as described in the
Django documentation on `Form Media <https://docs.djangoproject.com/en/1.3/topics/forms/media/>`_.
That means to include the javascript and css you need to make the widgets work you
can include ``{{ form.media.css }}`` and ``{{ form.media.js }}`` in your template. This is
assuming your form is called `form` in the template context. For more information
please check out the `Django documentation <https://docs.djangoproject.com/en/1.3/topics/forms/media/>`_.

The jQuery and jQuery UI libraries are not included in the distribution but must be included
in your templates. See the example project for an example using these libraries from the
`Google CDN <http://code.google.com/apis/libraries/devguide.html#jquery>`_. Django-Selectable
should work with `jQuery <http://jquery.com/>`_ >= 1.4.3 and `jQuery UI <http://jqueryui.com/>`_ >= 1.8

    .. literalinclude:: ../example/core/templates/base.html
        :start-after: {% block extra-css %}{% endblock %}
        :end-before: {% block extra-js %}


You must also include a `jQuery UI theme <http://jqueryui.com/themeroller/>`_ stylesheet. In the
example project we've included the "lightness" theme via the Google CDN.

    .. literalinclude:: ../example/core/templates/base.html
        :start-after: </title>
        :end-before: {% block extra-css %}


Defining a Lookup
--------------------------------

The lookup classes define the backend views. The most common case is defining a
lookup which searchs models based on a particular field. Let's define a simple model:

    .. literalinclude:: ../example/core/models.py
        :pyobject: Fruit

In a `lookups.py` we will define our lookup:

    .. literalinclude:: ../example/core/lookups.py
        :pyobject: FruitLookup

This lookups extends ``selectable.base.ModelLookup`` and defines two things: one is
the model on which we will be searching and the other is the field which we are searching.
This syntax should look familiar as it is the same as the `field lookup syntax <http://docs.djangoproject.com/en/1.3/ref/models/querysets/#field-lookups>`_
for making queries in Django.

Below this definition we will register our lookup class.

    .. code-block:: python

        registry.register(FruitLookup)

.. note::

    You should only register your lookup once. Attempting to register the same lookup class
    more than once will lead to ``LookupAlreadyRegistered`` errors. A common problem related to the
    ``LookupAlreadyRegistered`` error is related to inconsistant import paths in your project.
    Prior to Django 1.4 the default ``manage.py`` allows for importing both with and without
    the project name (i.e. ``from myproject.myapp import lookups`` or ``from myapp import lookups``).
    This leads to the ``lookup.py`` file being imported twice and the registration code
    executing twice. Thankfully this is no longer the default in Django 1.4. Keeping
    your import consistant to include the project name (when your app is included inside the
    project directory) will avoid these errors.


Defining Forms
--------------------------------

Now that we have a working lookup we will define a form which uses it:

    .. literalinclude:: ../example/core/forms.py
        :pyobject: FruitForm
        :end-before: newautocomplete

This replaces the default widget for the ``CharField`` with the ``AutoCompleteWidget``.
This will allow the user to fill this field with values taken from the names of
existing ``Fruit`` models.

And that's pretty much it. Keep on reading if you want to learn about the other
types of fields and widgets that are available as well as defining more complicated
lookups.
