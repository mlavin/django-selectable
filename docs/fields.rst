Fields
==========

Django-Selectable defines a number of fields for selecting either single or multiple
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

    .. code-block:: python

        from django import forms

        from selectable.forms import AutoCompleteSelectField

        from .lookups import FruitLookup


        class FruitSelectionForm(forms.Form):
            fruit = AutoCompleteSelectField(lookup_class=FruitLookup, label='Select a fruit')

`lookup_class`` may also be a dotted path.


.. _AutoCompleteSelectMultipleField:

AutoCompleteSelectMultipleField
--------------------------------------

Field tied to :ref:`AutoCompleteSelectMultipleWidget` to bind the selection to the form.
This field cleans to a list of items. :ref:`AutoCompleteSelectMultipleField` does not
allow for the creation of new items.


    .. code-block:: python

        from django import forms

        from selectable.forms import AutoCompleteSelectMultipleField

        from .lookups import FruitLookup


        class FruitsSelectionForm(forms.Form):
            fruits = AutoCompleteSelectMultipleField(lookup_class=FruitLookup,
                label='Select your favorite fruits')
