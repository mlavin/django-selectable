from django import forms

import selectable.forms as selectable

from example.core.lookups import FruitLookup


class FruitForm(forms.Form):
    autocomplete = forms.CharField(
        label='Type the name of a fruit (AutoCompleteWidget)',
        widget=selectable.AutoCompleteWidget(FruitLookup),
        required=False,
    )
    newautocomplete = forms.CharField(
        label='Type the name of a fruit (AutoCompleteWidget which allows new items)',
        widget=selectable.AutoCompleteWidget(FruitLookup, allow_new=True),
        required=False,
    )
    combobox = forms.CharField(
        label='Type/select the name of a fruit (AutoComboboxWidget)',
        widget=selectable.AutoComboboxWidget(FruitLookup),
        required=False,
    )
    newcombobox = forms.CharField(
        label='Type/select the name of a fruit (AutoComboboxWidget which allows new items)',
        widget=selectable.AutoComboboxWidget(FruitLookup, allow_new=True),
        required=False,
    )
    autocompleteselect = selectable.AutoCompleteSelectField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteField)',
        required=False,
    )
    newautocompleteselect = selectable.AutoCompleteSelectField(
        lookup_class=FruitLookup,
        allow_new=True,
        label='Select a fruit (AutoCompleteField which allows new items)',
        required=False,
    )
    comboboxselect = selectable.AutoComboboxSelectField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoComboboxSelectField)',
        required=False,
    )
    newcomboboxselect = selectable.AutoComboboxSelectField(
        lookup_class=FruitLookup,
        allow_new=True,
        label='Select a fruit (AutoComboboxSelectField which allows new items)',
        required=False,
    )
    multiautocompleteselect = selectable.AutoCompleteSelectMultipleField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteSelectMultipleField)',
        required=False,
    )
    multicomboboxselect = selectable.AutoComboboxSelectMultipleField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoComboboxSelectMultipleField)',
        required=False,
    )

