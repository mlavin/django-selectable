Release Notes
==================

v0.4.2 (Released 2012-06-08)
--------------------------------------

Bug Fixes
_________________

- Backported fix for double ``autocompleteselect`` event firing.
- Backported fix for broken pagination in search results.


v0.4.1 (Released 2012-03-11)
--------------------------------------

Bug Fixes
_________________

- Cleaned up whitespace in css/js. Thanks Dan Poirier for the report and fix.
- Fixed issue with saving M2M field data with AutoCompleteSelectMultipleField. Thanks Raoul Thill for the report.


v0.4.0 (Released 2012-02-25)
--------------------------------------

Features
_________________

- Better compatibility with :ref:`AutoCompleteSelectWidget`/:ref:`AutoComboboxSelectWidget` and Django's ModelChoiceField
- Better compatibility with the Django admin :ref:`add another popup <admin-basic-example>`
- Easier passing of query parameters. See the :ref:`Additional Parameters <additional-parameters>` section
- Additional documentation
- QUnit tests for JS functionality


Backwards Incompatible Changes
________________________________

- Support for ``ModelLookup.search_field`` string has been removed. You should use the ``ModelLookup.search_fields`` tuple instead.


v0.3.1 (Released 2012-02-23)
--------------------------------------

Bug Fixes
_________________

- Fixed issue with media urls when not using staticfiles.


v0.3.0 (Released 2012-02-15)
--------------------------------------

Features
_________________

- Multiple search fields for :ref:`model based lookups <ModelLookup>`
- Support for :ref:`highlighting term matches <javascript-highlightMatch>`
- Support for HTML in :ref:`result labels <lookup-get-item-label>`
- Support for :ref:`client side formatting <advanaced-label-formats>`
- Additional documentation
- Expanded examples in example project


Bug Fixes
_________________

- Fixed issue with Enter key removing items from select multiple widgets `#24 <https://bitbucket.org/mlavin/django-selectable/issue/24/pressing-enter-when-autocomplete-input-box>`_


Backwards Incompatible Changes
________________________________

- The fix for #24 changed the remove items from a button to an anchor tag. If you were previously using the button tag for additional styling then you will need to adjust your styles.
- The static resources were moved into a `selectable` sub-directory. This makes the media more in line with the template directory conventions. If you are using the widgets in the admin there is nothing to change. If you are using ``{{ form.media }}`` then there is also nothing to change. However if you were including static media manually then you will need to adjust them to include the selectable prefix.


v0.2.0 (Released 2011-08-13)
--------------------------------------

Features
_________________

- Additional documentation
- :ref:`Positional configuration <AutoCompleteSelectMultipleWidget>` for multiple select fields/widgets
- :ref:`Settings/configuration <SELECTABLE_MAX_LIMIT>` for limiting/paginating result sets
- Compatibility and examples for :ref:`Admin inlines <admin-inline-example>`
- JS updated for jQuery 1.6 compatibility
- :ref:`JS hooks <client-side-parameters>` for updating query parameters
- :ref:`Chained selection example <chain-select-example>`


v0.1.2 (Released 2011-05-25)
--------------------------------------

Bug Fixes
_________________

- Fixed issue `#17 <https://bitbucket.org/mlavin/django-selectable/issue/17/update-not-working>`_


v0.1.1 (Release 2011-03-21)
--------------------------------------

Bug Fixes
_________________

- Fixed/cleaned up multiple select fields and widgets
- Added media definitions to widgets


Features
_________________

- Additional documentation
- Added `update_query_parameters` to widgets
- Refactored JS for easier configuration


v0.1 (Released 2011-03-13)
--------------------------------------

Initial public release
