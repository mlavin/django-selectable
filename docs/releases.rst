Release Notes
==================


v1.2.0 (Released TBD)
--------------------------------------

Primarily a Django support related release. This version adds support for Django 2.0 and 2.1 while
dropping support for Django versions below 1.11. A number of deprecation warnings for future Django
versions have also been addressed.

Added the ability to search on multiple terms split by whitespace.


Backwards Incompatible Changes
________________________________

- Dropped support for Django versions below 1.11


  v1.1.0 (Released 2018-01-12)
--------------------------------------

- Updated admin docs.
- Added support for Django 1.11

Special thanks to Luke Plant for contributing the fixes to support Django 1.11.


v1.0.0 (Released 2017-04-14)
--------------------------------------

This project has been stable for quite some time and finally declaring a 1.0 release. With
that comes new policies on official supported versions for Django, Python, jQuery, and jQuery UI.

- New translations for German and Czech.
- Various bug and compatibility fixes.
- Updated example project.

Special thanks to Raphael Merx for helping track down issues related to this release
and an updating the example project to work on Django 1.10.

Backwards Incompatible Changes
________________________________

- Dropped support Python 2.6 and 3.2
- Dropped support for Django < 1.7. Django 1.11 is not yet supported.
- ``LookupBase.serialize_results`` had been removed. This is now handled by the built-in ``JsonResponse`` in Django.
- jQuery and jQuery UI versions for the ``include_jquery_libs`` and ``include_ui_theme`` template tags have been increased to 1.12.4 and 1.11.4 respectively.
- Dropped testing support for jQuery < 1.9 and jQuery UI < 1.10. Earlier versions may continue to work but it is recommended to upgrade.


v0.9.0 (Released 2014-10-21)
--------------------------------------

This release primarily addresses incompatibility with Django 1.7. The app-loading refactor both
broke the previous registration and at the same time provided better utilities in Django core to
make it more robust.

- Compatibility with Django 1.7. Thanks to Calvin Spealman for the fixes.
- Fixes for Python 3 support.

Backwards Incompatible Changes
________________________________

- Dropped support for jQuery < 1.7


v0.8.0 (Released 2014-01-20)
--------------------------------------

- Widget media references now include a version string for cache-busting when upgrading django-selectable. Thanks to Ustun Ozgur.
- Added compatibility code for \*SelectWidgets to handle POST data for the default SelectWidget. Thanks to leo-the-manic.
- Development moved from Bitbucket to Github.
- Update test suite compatibility with new test runner in Django 1.6. Thanks to Dan Poirier for the report and fix.
- Tests now run on Travis CI.
- Added French and Chinese translations.

Backwards Incompatible Changes
________________________________

- Support for Django < 1.5 has been dropped. Most pieces should continue to work but there was an ugly JS hack to make django-selectable work nicely in the admin which too flakey to continue to maintain. If you aren't using the selectable widgets in inline-forms in the admin you can most likely continue to use Django 1.4 without issue.


v0.7.0 (Released 2013-03-01)
--------------------------------------

This release features a large refactor of the JS plugin used by the widgets. While this
over makes the plugin more maintainable and allowed for some of the new features in this
release, it does introduce a few incompatible changes. For the most part places where you
might have previously used the ``autocomplete`` namespace/plugin, those references should
be updated to reference the ``djselectable`` plugin.

This release also adds experimental support for Python 3.2+ to go along with Django's support in 1.5.
To use Python 3 with django-selectable you will need to use Django 1.5+.

- Experimental Python 3.2+ support
- Improved the scope of ``prepareQuery`` and ``formatLabel`` options. Not fully backwards compatible. Thanks to Augusto Men.
- Allow passing the Python path string in place of the lookup class to the fields and widgets. Thanks to Michael Manfre.
- Allow passing JS plugin options through the widget ``attrs`` option. Thanks to Felipe Prenholato.
- Tests for compatibility with jQuery 1.6 through 1.9 and jQuery UI 1.8 through 1.10.
- Added notes on Bootstrap compatibility.
- Added compatibility with Grappelli in the admin.
- Added Spanish translation thanks to Manuel Alvarez.
- Added documentation notes on testing.

Bug Fixes
_________________

- Fixed bug with matching hidden input when the name contains '_1'. Thanks to Augusto Men for the report and fix.
- Fixed bug where the enter button would open the combobox options rather than submit the form. Thanks to Felipe Prenholato for the report.
- Fixed bug with using ``allow_new=True`` creating items when no data was submitted. See #91.
- Fixed bug with widget ``has_changed`` when there is no initial data. See #92.


Backwards Incompatible Changes
________________________________

- The JS event namespace has changed from ``autocomplete`` to ``djselectable``.
- ``data('autocomplete')`` is no longer available on the widgets on the client-side. Use ``data('djselectable')`` instead.
- Combobox button was changed from a ``<button>`` to ``<a>``. Any customized styles you may have should be updated.
- Combobox no longer changes the ``minLength`` or ``delay`` options.


v0.6.2 (Released 2012-11-07)
--------------------------------------

Bug Fixes
_________________

- Fixed bug with special characters when highlighting matches. Thanks to Chad Files for the report.
- Fixed javascript bug with spaces in ``item.id``. Thanks to @dc for the report and fix.


v0.6.1 (Released 2012-10-13)
--------------------------------------

Features
_________________

- Added Polish translation. Thanks to Sławomir Ehlert.

Bug Fixes
_________________

- Fixed incompatibility with jQuery UI 1.9.


v0.6.0 (Released 2012-10-09)
--------------------------------------

This release continues to clean up the API and JS. This was primarily motivated by
Sławomir Ehlert (@slafs) who is working on an alternate implementation which
uses Select2 rather than jQuery UI. This opens the door for additional apps
which use the same lookup declaration API with a different JS library on the front
end.

Python 2.5 support has been dropped to work towards Python 3 support.
This also drops Django 1.2 support which is no longer receiving security fixes.

Features
_________________

- Initial translations (pt_BR). Thanks to Felipe Prenholato for the patch.
- Upgraded default jQuery UI version included by the template tags from 1.8.18 to 1.8.23
- Added ``djselectableadd`` and ``djselectableremove`` events fired when items are added or removed from a mutliple select

Bug Fixes
_________________

- Cleaned up JS scoping problems when multiple jQuery versions are used on the page. Thanks Antti Kaihola for the report.
- Fixed minor JS bug where text input was not cleared when selected via the combobox in the multiselect. Thanks Antti Kaihola for the report and Lukas Pirl for a hotfix.

Backwards Incompatible Changes
________________________________

- ``get_item_value`` and ``get_item_id`` are no longer marked as safe by default.
- Removed AutoComboboxSelectField and AutoComboboxSelectMultipleField. These were deprecated in 0.5.
- Dropping official Python 2.5 support.
- Dropping official Django 1.2 support.
- ``paginate_results`` signature changed as part of the lookup refactor.
- ``SELECTABLE_MAX_LIMIT`` can no longer be ``None``.


v0.5.2 (Released 2012-06-27)
--------------------------------------

Bug Fixes
_________________

- Fixed XSS flaw with lookup ``get_item_*`` methods. Thanks slafs for the report.
- Fixed bug when passing widget instance rather than widget class to ``AutoCompleteSelectField`` or ``AutoCompleteSelectMultipleField``.


v0.5.1 (Released 2012-06-08)
--------------------------------------

Bug Fixes
_________________

- Fix for double ``autocompleteselect`` event firing.
- Fix for broken pagination in search results. Thanks David Ray for report and fix.


v0.4.2 (Released 2012-06-08)
--------------------------------------

Bug Fixes
_________________

- Backported fix for double ``autocompleteselect`` event firing.
- Backported fix for broken pagination in search results.


v0.5.0 (Released 2012-06-02)
--------------------------------------

Features
_________________

- Template tag to add necessary jQuery and jQuery UI libraries. Thanks to Rick Testore for the initial implementation
- :ref:`Lookup decorators <lookup-decorators>` for requiring user authentication or staff access to use the lookup
- Additional documentation
- Minor updates to the example project

Backwards Incompatible Changes
________________________________

- Previously the minimal version of jQuery was listed as 1.4.3 when it fact there was a bug a that made django-selectable require 1.4.4. Not a new incompatibility but the docs have now been updated and 1.4.3 compatibility will not be added. Thanks to Rick Testore for the report and the fix
- Started deprecation path for AutoComboboxSelectField and AutoComboboxSelectMultipleField


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
- Support for :ref:`client side formatting <advanced-label-formats>`
- Additional documentation
- Expanded examples in example project


Bug Fixes
_________________

- Fixed issue with Enter key removing items from select multiple widgets `#24 <https://github.com/mlavin/django-selectable/issues/24>`_


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

- Fixed issue `#17 <https://github.com/mlavin/django-selectable/issues/17>`_


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
