from django import forms
from django.forms.models import modelformset_factory
from django.contrib.localflavor.us.forms import USStateField, USStateSelect

import selectable.forms as selectable

from example.core.lookups import FruitLookup, CityLookup
from example.core.models import Farm


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
    # AutoCompleteSelectField (no new items)
    autocompleteselect = selectable.AutoCompleteSelectField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteField)',
        required=False,
    )
    # AutoCompleteSelectField (allows new items)
    newautocompleteselect = selectable.AutoCompleteSelectField(
        lookup_class=FruitLookup,
        allow_new=True,
        label='Select a fruit (AutoCompleteField which allows new items)',
        required=False,
    )
    # AutoComboboxSelectField (no new items)
    comboboxselect = selectable.AutoComboboxSelectField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoComboboxSelectField)',
        required=False,
    )
    # AutoComboboxSelectField (allows new items)
    newcomboboxselect = selectable.AutoComboboxSelectField(
        lookup_class=FruitLookup,
        allow_new=True,
        label='Select a fruit (AutoComboboxSelectField which allows new items)',
        required=False,
    )
    # AutoCompleteSelectMultipleField
    multiautocompleteselect = selectable.AutoCompleteSelectMultipleField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteSelectMultipleField)',
        required=False,
    )
    # AutoComboboxSelectMultipleField
    multicomboboxselect = selectable.AutoComboboxSelectMultipleField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoComboboxSelectMultipleField)',
        required=False,
    )


class ChainedForm(forms.Form):
    city = selectable.AutoComboboxSelectField(
        lookup_class=CityLookup,
        label='City',
        required=False,
    )
    state = USStateField(widget=USStateSelect, required=False)


class FarmForm(forms.ModelForm):

    class Meta(object):
        model = Farm
        widgets = {
            'fruit': selectable.AutoCompleteSelectMultipleWidget(lookup_class=FruitLookup),
        }


FarmFormset = modelformset_factory(Farm, FarmForm)

