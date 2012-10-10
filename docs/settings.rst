Settings
==================


.. _SELECTABLE_MAX_LIMIT:

SELECTABLE_MAX_LIMIT
--------------------------------------

This setting is used to limit the number of results returned by the auto-complete fields.
Each field/widget can individually lower this maximum. The result sets will be
paginated allowing the client to ask for more results. The limit is passed as a
query parameter and validated against this value to ensure the client cannot manipulate
the query string to retrive more values.

Default: ``25``


.. versionadded:: 0.6

.. _SELECTABLE_ESCAPED_KEYS:

SELECTABLE_ESCAPED_KEYS
--------------------------------------

The ``LookupBase.format_item`` will conditionally escape result keys based on this
setting. The label is escaped by default to prevent a XSS flaw when using the
jQuery UI autocomplete. If you are using the lookup responses for a different
autocomplete plugin then you may need to esacpe more keys by default.

Default: ``('label', )``

.. note::
    You probably don't want to include ``id`` in this setting.


.. _javascript-options:

Javascript Plugin Options
--------------------------------------

Below the options for configuring the Javascript behavior of the django-selectable
widgets.


.. _javascript-removeIcon:

removeIcon
______________________________________


This is the class name used for the remove buttons for the multiple select widgets.
The set of icon classes built into the jQuery UI framework can be found here:
http://jqueryui.com/themeroller/

Default: ``ui-icon-close``


.. _javascript-comboboxIcon:

comboboxIcon
______________________________________


This is the class name used for the combobox dropdown icon. The set of icon classes built 
into the jQuery UI framework can be found here: http://jqueryui.com/themeroller/

Default: ``ui-icon-triangle-1-s``


.. _javascript-prepareQuery:

prepareQuery
______________________________________


``prepareQuery`` is a function that is run prior to sending the search request to
the server. It is an oppotunity to add additional parameters to the search query.
It takes one argument which is the current search parameters as a dictionary. For
more information on its usage see :ref:`Adding Parameters on the Client Side <client-side-parameters>`.

Default: ``null``


.. _javascript-highlightMatch:

highlightMatch
______________________________________


If true the portions of the label which match the current search term will be wrapped
in a span with the class ``highlight``.

Default: ``true``


.. _javascript-formatLabel:

formatLabel
______________________________________


``formatLabel`` is a function that is run prior to rendering the search results in
the dropdown menu. It takes two arguments: the current item label and the item data
dictionary. It should return the label which should be used. For more information
on its usage see :ref:`Label Formats on the Client Side <advanced-label-formats>`.

Default: ``null``

