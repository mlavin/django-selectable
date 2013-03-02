Widgets
==========

Below are the custom widgets defined by Django-Selectable. All widgets take the
lookup class as the first required argument.

These widgets all support a ``query_params`` keyword argument which is used to pass
additional query parameters to the lookup search. See the section on
:ref:`Adding Parameters on the Server Side <server-side-parameters>` for more
information.

.. versionadded:: 0.7

You can configure the plugin options by passing the configuration dictionary in the ``data-selectable-options``
attribute. The set of options availble include those define by the base
`autocomplete plugin <http://api.jqueryui.com/1.9/autocomplete/>`_ as well as the
:ref:`javascript-removeIcon`, :ref:`javascript-comboboxIcon`, and :ref:`javascript-highlightMatch` options
which are unique to django-selectable.

    .. code-block:: python

        attrs = {'data-selectable-options': {'highlightMatch': True, 'minLength': 5}}
        selectable.AutoCompleteSelectWidget(lookup_class=FruitLookup, attrs=attrs)


.. _AutoCompleteWidget:

AutoCompleteWidget
--------------------------------------

Basic widget for auto-completing text. The widget returns the item value as defined
by the lookup ``get_item_value``. If the ``allow_new`` keyword argument is passed as
true it will allow the user to type any text they wish.

.. _AutoComboboxWidget:

AutoComboboxWidget
--------------------------------------

Similar to :ref:`AutoCompleteWidget` but has a button to reveal all options.


.. _AutoCompleteSelectWidget:

AutoCompleteSelectWidget
--------------------------------------

Widget for selecting a value/id based on input text. Optionally allows selecting new items to be created.
This widget should be used in conjunction with the :ref:`AutoCompleteSelectField` as it will
return both the text entered by the user and the id (if an item was selected/matched).

:ref:`AutoCompleteSelectWidget` works directly with Django's
`ModelChoiceField <https://docs.djangoproject.com/en/1.3/ref/forms/fields/#modelchoicefield>`_.
You can simply replace the widget without replacing the entire field.

    .. code-block:: python

        class FarmAdminForm(forms.ModelForm):

            class Meta(object):
                model = Farm
                widgets = {
                    'owner': selectable.AutoCompleteSelectWidget(lookup_class=FruitLookup),
                }

The one catch is that you must use ``allow_new=False`` which is the default.

.. versionadded:: 0.7

``lookup_class`` may also be a dotted path.

    .. code-block:: python

         widget = selectable.AutoCompleteWidget(lookup_class='core.lookups.FruitLookup')


.. _AutoComboboxSelectWidget:

AutoComboboxSelectWidget
--------------------------------------

Similar to :ref:`AutoCompleteSelectWidget` but has a button to reveal all options.

:ref:`AutoComboboxSelectWidget` works directly with Django's
`ModelChoiceField <https://docs.djangoproject.com/en/1.3/ref/forms/fields/#modelchoicefield>`_.
You can simply replace the widget without replacing the entire field.

    .. code-block:: python

        class FarmAdminForm(forms.ModelForm):

            class Meta(object):
                model = Farm
                widgets = {
                    'owner': selectable.AutoComboboxSelectWidget(lookup_class=FruitLookup),
                }

The one catch is that you must use ``allow_new=False`` which is the default.


.. _AutoCompleteSelectMultipleWidget:

AutoCompleteSelectMultipleWidget
--------------------------------------

Builds a list of selected items from auto-completion. This widget will return a list
of item ids as defined by the lookup ``get_item_id``. Using this widget with the
:ref:`AutoCompleteSelectMultipleField` will clean the items to the item objects. This does
not allow for creating new items. There is another optional keyword argument ``postion``
which can take four possible values: `bottom`, `bottom-inline`, `top` or `top-inline`.
This determine the position of the deck list of currently selected items as well as
whether this list is stacked or inline. The default is `bottom`.


.. _AutoComboboxSelectMultipleWidget:

AutoComboboxSelectMultipleWidget
--------------------------------------

Same as :ref:`AutoCompleteSelectMultipleWidget` but with a combobox.
