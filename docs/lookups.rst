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

    from selectable.base import BaseLookup
    from selectable.registry import registry

    class MyLookup(BaseLookup):
        def get_query(self, request, term):
            data = ['Foo', 'Bar']
            return filter(lambda x: x.startswith(term), data)

    registry.register(MyLookup)


Lookup API
--------------------------------------

.. py:method:: BaseLookup.get_query(request, term)

    This is the main method which takes the current request
    from the user and returns the data which matches their search.

    :param request: The current request object
    :param term: The search term from the widget input
    :return: An iterable set of data of items matching the search term

.. py:method:: BaseLookup.get_item_label(item)

    This is first of three formatting methods. The label is shown in the
    drop down menu of search results. This defaults to `item.__unicode__`.

    :param item: An item from the search results.
    :return: A string representation of the item to be shown in the search results.

.. py:method:: BaseLookup.get_item_id(item)

    This is second of three formatting methods. The id is the value that will eventually
    be returned by the field/widget. This defaults to `item.__unicode__`.

    :param item: An item from the search results.
    :return: A string representation of the item to be returned by the field/widget.

.. py:method:: BaseLookup.get_item_value(item)

    This is last of three formatting methods. The value is shown in the
    input once the item has been selected. This defaults to `item.__unicode__`.

    :param item: An item from the search results.
    :return: A string representation of the item to be shown in the input.

.. py:method:: BaseLookup.get_item(value)

    `get_item` is the reverse of `get_item_id`. This should take the value
    from the form initial values and return the current item. This defaults
    to simply return the value.

    :param value: Value from the form inital value.
    :return: The item corresponding to the initial value.

