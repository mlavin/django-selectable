django-selectable
===================

Tools and widgets for using/creating auto-complete selection widgets using Django and jQuery UI.

Features
==========
Widgets
---------
`AutoCompleteWidget`
    Basic widget for auto-completing text.
`AutoComboboxWidget`
    Similar to `AutoCompleteWidget` but has a button to reveal all options.
`AutoCompleteSelectWidget`
    Widget for selecting a value/id based on input text. Optionally allows
    selecting new items to be created.
`AutoComboboxSelectWidget`
    Similar to `AutoCompleteSelectWidget` but has a button to reveal all options.
`AutoCompleteSelectMultipleWidget`
    Builds a list of selected items from auto-completion.
`AutoComboboxSelectMultipleWidget`
    Same as `AutoCompleteSelectMultipleWidget` but with a combobox.

Fields
---------
`AutoCompleteSelectField`
    Field tied to `AutoCompleteSelectWidget` to bind the selection to the form and
    create new items, if allowed.
`AutoComboboxSelectField`
    Field tied to `AutoComboboxSelectWidget` to bind the selection to the form and
    create new items, if allowed.
`AutoCompleteSelectMultipleField`
    Field tied to `AutoCompleteSelectMultipleWidget` to bind the selection to the form.
`AutoComboboxSelectMultipleField`
    Field tied to `AutoComboboxSelectMultipleWidget` to bind the selection to the form.


Dependencies
==============
Required
----------
- `Django <http://www.djangoproject.com/>`_ >= 1.2
- `jQuery <http://jquery.com/>`_ >= 1.4
- `jQuery UI <http://jqueryui.com/>`_ >= 1.8
