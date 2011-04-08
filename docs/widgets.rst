Widgets
==========

Below are the custom widgets defined by Django-Selectable. All widgets take the 
lookup class as the first required argument.


AutoCompleteWidget
--------------------------------------

Basic widget for auto-completing text. The widget returns the item value as defined
by the lookup `get_item_value`. If the `allow_new` keyword argument is passed as
true it will allow the user to type any text they wish.


AutoComboboxWidget
--------------------------------------

Similar to `AutoCompleteWidget` but has a button to reveal all options.


AutoCompleteSelectWidget
--------------------------------------

Widget for selecting a value/id based on input text. Optionally allows selecting new items to be created.
This widget should be used in conjunction with the `AutoCompleteSelectField` as it will
return both the text entered by the user and the id (if an item was selected/matched).


AutoComboboxSelectWidget
--------------------------------------

Similar to `AutoCompleteSelectWidget` but has a button to reveal all options.


AutoCompleteSelectMultipleWidget
--------------------------------------

Builds a list of selected items from auto-completion. This widget will return a list
of item ids as defined by the lookup `get_item_id`. Using this widget with the
`AutoCompleteSelectMultipleField` will clean the items to the item objects. This does
not allow for creating new items. There is another optional keyword argument `postion`
which can take four possible values: `bottom`, `bottom-inline`, `top` or `top-inline`.
This determine the position of the deck list of currently selected items as well as
whether this list is stacked or inline. The default is `bottom`.


AutoComboboxSelectMultipleWidget
--------------------------------------

Same as `AutoCompleteSelectMultipleWidget` but with a combobox.
