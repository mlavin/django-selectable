Settings
==================


.. _SELECTABLE_MAX_LIMIT:

SELECTABLE_MAX_LIMIT
--------------------------------------

.. versionadded:: 0.2

This setting is used to limit the number of results returned by the auto-complete fields.
Each field/widget can individually lower this maximum. The result sets will be
paginated allowing the client to ask for more results. The limit is passed as a
query parameter and validated against this value to ensure the client cannot manipulate
the query string to retrive more values.

You may disable this global maximum by setting

.. code-block:: python

    SELECTABLE_MAX_LIMIT = None

Default: 25

