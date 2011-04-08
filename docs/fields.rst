Fields
==========

Django-Selectable defines a number of fields for selecting either single or mutliple
lookup items. Item in this context corresponds to the object return by the underlying
lookup `get_item`. The single select select fields (`AutoCompleteSelectField` and
`AutoComboboxSelectField`) allow for the creation of new items. To use this feature the field's
lookup class must define `create_item`. In the case of lookups extending from
`ModelLookup` newly created items have not yet been saved into the database and saving
should be handled by the form. All fields take the lookup class as the first required
argument.


AutoCompleteSelectField
--------------------------------------
    
Field tied to `AutoCompleteSelectWidget` to bind the selection to the form and  
create new items, if allowed. The `allow_new` keyword argument (default: `False`)
which determines if the field allows new items. This field cleans to a single item.


AutoComboboxSelectField
--------------------------------------

Field tied to `AutoComboboxSelectWidget` to bind the selection to the form and 
create new items, if allowed. The `allow_new` keyword argument (default: `False`)
which determines if the field allows new items. This field cleans to a single item.


AutoCompleteSelectMultipleField
--------------------------------------

Field tied to `AutoCompleteSelectMultipleWidget` to bind the selection to the form.
This field cleans to a list of items. `AutoCompleteSelectMultipleField` does not
allow for the creation of new items.


AutoComboboxSelectMultipleField
--------------------------------------

Field tied to `AutoComboboxSelectMultipleWidget` to bind the selection to the form.
This field cleans to a list of items. `AutoComboboxSelectMultipleField` does not 
allow for the creation of new items.
