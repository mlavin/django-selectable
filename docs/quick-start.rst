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
in your templates. However there is a template tag to easily add these libraries from
the  from the `Google CDN <http://code.google.com/apis/libraries/devguide.html#jquery>`_.

    .. code-block:: html

        {% load selectable_tags %}
        {% include_jquery_libs %}

By default these will use jQuery v1.7.2 and jQuery UI v1.8.23. You can customize the versions
used by pass them to the tag. The first version is the jQuery version and the second is the
jQuery UI version.

    .. code-block:: html

        {% load selectable_tags %}
        {% include_jquery_libs '1.4.4' '1.8.13' %}

Django-Selectable should work with `jQuery <http://jquery.com/>`_ >= 1.4.4 and
`jQuery UI <http://jqueryui.com/>`_ >= 1.8.13.

You must also include a `jQuery UI theme <http://jqueryui.com/themeroller/>`_ stylesheet. There
is also a template tag to easily add this style sheet from the Google CDN.

    .. code-block:: html

        {% load selectable_tags %}
        {% include_ui_theme %}

By default this will use the `base <http://jqueryui.com/themeroller/>`_ theme for jQuery UI v1.8.23.
You can configure the theme and version by passing them in the tag.

    .. code-block:: html

        {% load selectable_tags %}
        {% include_ui_theme 'ui-lightness' '1.8.13' %}

Or only change the theme.

    .. code-block:: html

        {% load selectable_tags %}
        {% include_ui_theme 'ui-lightness' %}

See the the jQuery UI documentation for a full list of available stable themes: http://jqueryui.com/download#stable-themes

Of course you can choose to include these rescources manually::

    .. code-block:: html

        <link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.0/themes/base/jquery-ui.css" type="text/css">
        <link href="{{ STATIC_URL }}selectable/css/dj.selectable.css" type="text/css" media="all" rel="stylesheet">
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.0/jquery-ui.js"></script>
        <script type="text/javascript" src="{{ STATIC_URL }}selectable/js/jquery.dj.selectable.js"></script>

.. note::

    jQuery UI shares a few plugin names with the popular Twitter Bootstrap framework. There
    are notes on using Bootstrap along with django-selectable in the :ref:`advanced usage
    section <advanced-bootstrap>`.


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
