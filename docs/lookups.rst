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
`selectable.base.LookupBase` which defines the API for every lookup.

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

    :param request: The current request object
    :param term: The search term from the widget input
    :return: An iterable set of data of items matching the search term

.. py:method:: LookupBase.get_item_label(item)

    This is first of three formatting methods. The label is shown in the
    drop down menu of search results. This defaults to `item.__unicode__`.

    :param item: An item from the search results.
    :return: A string representation of the item to be shown in the search results.

.. py:method:: LookupBase.get_item_id(item)

    This is second of three formatting methods. The id is the value that will eventually
    be returned by the field/widget. This defaults to `item.__unicode__`.

    :param item: An item from the search results.
    :return: A string representation of the item to be returned by the field/widget.

.. py:method:: LookupBase.get_item_value(item)

    This is last of three formatting methods. The value is shown in the
    input once the item has been selected. This defaults to `item.__unicode__`.

    :param item: An item from the search results.
    :return: A string representation of the item to be shown in the input.

.. py:method:: LookupBase.get_item(value)

    `get_item` is the reverse of `get_item_id`. This should take the value
    from the form initial values and return the current item. This defaults
    to simply return the value.

    :param value: Value from the form inital value.
    :return: The item corresponding to the initial value.

.. py:method:: LookupBase.create_item(value)

    If you plan to use a lookup with a field or widget which allows the user
    to input new values then you must define what it means to create a new item
    for your lookup. By default this raises a `NotImplemented` error.

    :param value: The user given value.
    :return: The new item created from the item.

.. py:method:: LookupBase.format_item(item)

    By default `format_item` creates a dictionary with the three keys used by
    the UI plugin: id, value, label. These are generated from the calls to
    `get_item_id`, `get_item_value`, and `get_item_label`. If you want to
    add additional keys you should add them here.

    :param item: An item from the search results.
    :return: A dictionary of information for this item to be sent back to the client.


Lookups Based on Models
--------------------------------------

Perhaps the most common use case is to define a lookup based on a given Django model.
For this you can extend `selectable.base.ModelLookup`. To extend `ModelLookup` you
should set two class attributes: `model` and `search_field`.

    .. literalinclude:: ../example/core/lookups.py
        :pyobject: FruitLookup

The syntax for `search_field` is the same as the Django 
`field lookup syntax <http://docs.djangoproject.com/en/1.3/ref/models/querysets/#field-lookups>`_. 
You may optionally define a third class attribute `filters` which is a dictionary of
filters to be applied to the model queryset. The keys should be a string defining a field lookup
and the value should be the value for the field lookup.

