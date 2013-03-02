Fields
==========

Django-Selectable defines a number of fields for selecting either single or mutliple
lookup items. Item in this context corresponds to the object return by the underlying
lookup ``get_item``. The single select select field :ref:`AutoCompleteSelectField`
allows for the creation of new items. To use this feature the field's
lookup class must define ``create_item``. In the case of lookups extending from
:ref:`ModelLookup` newly created items have not yet been saved into the database and saving
should be handled by the form. All fields take the lookup class as the first required
argument.


.. _AutoCompleteSelectField:

AutoCompleteSelectField
--------------------------------------

Field tied to :ref:`AutoCompleteSelectWidget` to bind the selection to the form and
create new items, if allowed. The ``allow_new`` keyword argument (default: ``False``)
which determines if the field allows new items. This field cleans to a single item.

    .. literalinclude:: ../example/core/forms.py
        :start-after: # AutoCompleteSelectField (no new items)
        :end-before: # AutoCompleteSelectField (allows new items)


.. versionadded:: 0.7

`lookup_class`` may also be a dotted path.

    .. code-block:: python

	    selectable.AutoCompleteSelectField(lookup_class='core.lookups.FruitLookup')


.. _AutoCompleteSelectMultipleField:

AutoCompleteSelectMultipleField
--------------------------------------

Field tied to :ref:`AutoCompleteSelectMultipleWidget` to bind the selection to the form.
This field cleans to a list of items. :ref:`AutoCompleteSelectMultipleField` does not
allow for the creation of new items.

    .. literalinclude:: ../example/core/forms.py
        :start-after: # AutoCompleteSelectMultipleField
        :end-before: # AutoComboboxSelectMultipleField
