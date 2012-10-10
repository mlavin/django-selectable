Defining Lookups
==================

What are Lookups?
--------------------------------------

Lookups define the corresponding ajax views used by the auto-completion
fields and widgets. They take in the current request and return the JSON
needed by the jQuery auto-complete plugin.


Defining a Lookup
--------------------------------------

django-selectable uses a registration pattern similar to the Django admin.
Lookups should be defined in a `lookups.py` in your application's module. Once defined
you must register in with django-selectable. All lookups must extend from
``selectable.base.LookupBase`` which defines the API for every lookup.

    .. code-block:: python

        from selectable.base import LookupBase
        from selectable.registry import registry

        class MyLookup(LookupBase):
            def get_query(self, request, term):
                data = ['Foo', 'Bar']
                return filter(lambda x: x.startswith(term), data)

        registry.register(MyLookup)


Lookup API
--------------------------------------

.. py:method:: LookupBase.get_query(request, term)

    This is the main method which takes the current request
    from the user and returns the data which matches their search.

    :param request: The current request object.
    :param term: The search term from the widget input.
    :return: An iterable set of data of items matching the search term.

.. _lookup-get-item-label:

.. py:method:: LookupBase.get_item_label(item)

    This is first of three formatting methods. The label is shown in the
    drop down menu of search results. This defaults to ``item.__unicode__``.

    :param item: An item from the search results.
    :return: A string representation of the item to be shown in the search results.
        The label can include HTML. For changing the label format on the client side
        see :ref:`Advanced Label Formats <advanced-label-formats>`.


.. py:method:: LookupBase.get_item_id(item)

    This is second of three formatting methods. The id is the value that will eventually
    be returned by the field/widget. This defaults to ``item.__unicode__``.

    :param item: An item from the search results.
    :return: A string representation of the item to be returned by the field/widget.

.. py:method:: LookupBase.get_item_value(item)

    This is last of three formatting methods. The value is shown in the
    input once the item has been selected. This defaults to ``item.__unicode__``.

    :param item: An item from the search results.
    :return: A string representation of the item to be shown in the input.

.. py:method:: LookupBase.get_item(value)

    ``get_item`` is the reverse of ``get_item_id``. This should take the value
    from the form initial values and return the current item. This defaults
    to simply return the value.

    :param value: Value from the form inital value.
    :return: The item corresponding to the initial value.

.. py:method:: LookupBase.create_item(value)

    If you plan to use a lookup with a field or widget which allows the user
    to input new values then you must define what it means to create a new item
    for your lookup. By default this raises a ``NotImplemented`` error.

    :param value: The user given value.
    :return: The new item created from the item.

.. _lookup-format-item:

.. py:method:: LookupBase.format_item(item)

    By default ``format_item`` creates a dictionary with the three keys used by
    the UI plugin: id, value, label. These are generated from the calls to
    ``get_item_id``, ``get_item_value`` and ``get_item_label``. If you want to
    add additional keys you should add them here.

    The results of ``get_item_label`` is conditionally escaped to prevent
    Cross Site Scripting (XSS) similar to the templating language.
    If you know that the content is safe and you want to use these methods
    to include HTML should mark the content as safe with ``django.utils.safestring.mark_safe``
    inside the ``get_item_label`` method.

    ``get_item_id`` and ``get_item_value`` are not escapted by default. These are
    not a XSS vector with the built-in JS. If you are doing additional formating using
    these values you should be conscience of this fake and be sure to escape these
    values.

    :param item: An item from the search results.
    :return: A dictionary of information for this item to be sent back to the client.

There are also some additional methods that you could want to use/override. These
are for more advanced use cases such as using the lookups with JS libraries other
than jQuery UI. Most users will not need to override these methods.

.. _lookup-format-results:

.. py:method:: LookupBase.format_results(self, raw_data, options)

    Returns a python structure that later gets serialized. This makes a call to
    :ref:`paginate_results<lookup-paginate-results>` prior to calling
    :ref:`format_item<lookup-format-item>` on each item in the current page.

    :param raw_data: The set of all matched results.
    :param options: Dictionary of ``cleaned_data`` from the lookup form class.
    :return: A dictionary with two keys ``meta`` and ``data``.
        The value of ``data`` is an iterable extracted from page_data.
        The value of ``meta`` is a dictionary. This is a copy of options with one additional element
        ``more`` which is a translatable "Show more" string
        (useful for indicating more results on the javascript side).

.. _lookup-paginate-results:

.. py:method:: LookupBase.paginate_results(results, options)

    If :ref:`SELECTABLE_MAX_LIMIT` is defined or ``limit`` is passed in request.GET
    then ``paginate_results`` will return the current page using Django's
    built in pagination. See the Django docs on
    `pagination <https://docs.djangoproject.com/en/1.3/topics/pagination/>`_
    for more info.

    :param results: The set of all matched results.
    :param options: Dictionary of ``cleaned_data`` from the lookup form class.
    :return: The current `Page object <https://docs.djangoproject.com/en/1.3/topics/pagination/#page-objects>`_
        of results.

.. _lookup-serialize-results:

.. py:method:: LookupBase.serialize_results(self, results)

    Returns serialized results for sending via http. You may choose to override
    this if you are making use of 

    :param results: a python structure to be serialized e.g. the one returned by :ref:`format_results<lookup-format-results>`
    :returns: JSON string.


.. _ModelLookup:

Lookups Based on Models
--------------------------------------

Perhaps the most common use case is to define a lookup based on a given Django model.
For this you can extend ``selectable.base.ModelLookup``. To extend ``ModelLookup`` you
should set two class attributes: ``model`` and ``search_fields``.

    .. literalinclude:: ../example/core/lookups.py
        :pyobject: FruitLookup

The syntax for ``search_fields`` is the same as the Django
`field lookup syntax <http://docs.djangoproject.com/en/1.3/ref/models/querysets/#field-lookups>`_.
Each of these lookups are combined as OR so any one of them matching will return a
result. You may optionally define a third class attribute ``filters`` which is a dictionary of
filters to be applied to the model queryset. The keys should be a string defining a field lookup
and the value should be the value for the field lookup. Filters on the other hand are
combined with AND.


User Lookup Example
--------------------------------------

Below is a larger model lookup example using multiple search fields, filters
and display options for the `auth.User <https://docs.djangoproject.com/en/1.3/topics/auth/#users>`_
model.

    .. code-block:: python

        from django.contrib.auth.models import User
        from selectable.base import ModelLookup
        from selectable.registry import registry


        class UserLookup(ModelLookup):
            model = User
            search_fields = (
                'username__icontains',
                'first_name__icontains',
                'last_name__icontains',
            )
            filters = {'is_active': True, }

            def get_item_value(self, item):
                # Display for currently selected item
                return item.username

            def get_item_label(self, item):
                # Display for choice listings
                return u"%s (%s)" % (item.username, item.get_full_name())

        registry.register(UserLookup)


.. _lookup-decorators:

Lookup Decorators
--------------------------------------

.. versionadded:: 0.5

Registering lookups with django-selectable creates a small API for searching the
lookup data. While the amount of visible data is small there are times when you want
to restrict the set of requests which can view the data. For this purpose there are
lookup decorators. To use them you simply decorate your lookup class.

    .. code-block:: python

        from django.contrib.auth.models import User
        from selectable.base import ModelLookup
        from selectable.decorators import login_required
        from selectable.registry import registry


        @login_required
        class UserLookup(ModelLookup):
            model = User
            search_fields = ('username__icontains', )
            filters = {'is_active': True, }

        registry.register(UserLookup)

.. note::

    The class decorator syntax was introduced in Python 2.6. If you are using
    django-selectable with Python 2.5 you can still make use of these decorators
    by applying the without the decorator syntax.

    .. code-block:: python

        class UserLookup(ModelLookup):
            model = User
            search_fields = ('username__icontains', )
            filters = {'is_active': True, }

        UserLookup = login_required(UserLookup)

        registry.register(UserLookup)

Below are the descriptions of the available lookup decorators.


ajax_required
______________________________________

The django-selectable javascript will always request the lookup data via
XMLHttpRequest (AJAX) request. This decorator enforces that the lookup can only
be accessed in this way. If the request is not an AJAX request then it will return
a 400 Bad Request response.


login_required
______________________________________

This decorator requires the user to be authenticated via ``request.user.is_authenticated``.
If the user is not authenticated this will return a 401 Unauthorized response.
``request.user`` is set by the ``django.contrib.auth.middleware.AuthenticationMiddleware``
which is required for this decorator to work. This middleware is enabled by default.

staff_member_required
______________________________________

This decorator builds from ``login_required`` and in addition requires that
``request.user.is_staff`` is ``True``. If the user is not authenticatated this will
continue to return at 401 response. If the user is authenticated but not a staff member
then this will return a 403 Forbidden response.
