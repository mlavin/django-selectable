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

The jQuery and jQuery UI libraries are not included in the distribution but must be included
in your templates. See the example project for an example using these libraries from the
`Google CDN <http://code.google.com/apis/libraries/devguide.html#jquery>`_. Django-Selectable
should work with `jQuery <http://jquery.com/>`_ >= 1.4.3 and `jQuery UI <http://jqueryui.com/>`_ >= 1.8

    .. literalinclude:: ../example/core/templates/base.html
        :start-after: {{ form.media.css }}
        :end-before: {{ form.media.js }}


You must also include a `jQuery UI theme <http://jqueryui.com/themeroller/>`_ stylesheet. In the
example project we've included the "lightness" theme via the Google CDN.

    .. literalinclude:: ../example/core/templates/base.html
        :start-after: </title>
        :end-before: {{ form.media.css }}


Defining a Lookup
--------------------------------

The lookup classes define the backend views. The most common case is defining a
lookup which searchs models based on a particular field. Let's define a simple model:

    .. literalinclude:: ../example/core/models.py
        :pyobject: Fruit

In a `lookups.py` we will define our lookup:

    .. literalinclude:: ../example/core/lookups.py
        :pyobject: FruitLookup

This lookups extends `selectable.base.ModelLookup` and defines two things: one is
the model on which we will be searching and the other is the field which we are searching.
This syntax should look familiar as it is the same as the `field lookup syntax <http://docs.djangoproject.com/en/1.3/ref/models/querysets/#field-lookups>`_
for making queries in Django.

Below this definition we will register our lookup class.

    .. code-block:: python

        registry.register(FruitLookup)


Defining Forms
--------------------------------

Now that we have a working lookup we will define a form which uses it:

    .. literalinclude:: ../example/core/forms.py
        :pyobject: FruitForm
        :end-before: newautocomplete

This replaces the default widget for the `CharField` with the `AutoCompleteWidget`.
This will allow the user to fill this field with values taken from the names of
existing `Fruit` models.

And that's pretty much it. Keep on reading if you want to learn about the other
types of fields and widgets that are available as well as defining more complicated
lookups.