from django import forms
from django.forms.models import modelformset_factory

try:
    from localflavor.us.forms import USStateField, USStateSelect
except ImportError:
    from django.contrib.localflavor.us.forms import USStateField, USStateSelect

import selectable.forms as selectable

from core.lookups import FruitLookup, CityLookup
from core.models import Farm


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
    # AutoCompleteSelectField (no new items)
    comboboxselect = selectable.AutoCompleteSelectField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteSelectField with combobox)',
        required=False,
        widget=selectable.AutoComboboxSelectWidget
    )
    # AutoComboboxSelect (allows new items)
    newcomboboxselect = selectable.AutoCompleteSelectField(
        lookup_class=FruitLookup,
        allow_new=True,
        label='Select a fruit (AutoCompleteSelectField with combobox which allows new items)',
        required=False,
        widget=selectable.AutoComboboxSelectWidget
    )
    # AutoCompleteSelectMultipleField
    multiautocompleteselect = selectable.AutoCompleteSelectMultipleField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteSelectMultipleField)',
        required=False,
    )
    # AutoComboboxSelectMultipleField
    multicomboboxselect = selectable.AutoCompleteSelectMultipleField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteSelectMultipleField with combobox)',
        required=False,
        widget=selectable.AutoComboboxSelectMultipleWidget
    )
    # AutoComboboxSelectMultipleField with disabled attribute
    disabledmulticomboboxselect = selectable.AutoCompleteSelectMultipleField(
        lookup_class=FruitLookup,
        label='Disabled Selectable field',
        required=False,
        widget=selectable.AutoComboboxSelectMultipleWidget,
        initial={'1', '2'},
    )

    def __init__(self, *args, **kwargs):
        super(FruitForm, self).__init__(*args, **kwargs)
        self.fields['disabledmulticomboboxselect'].widget.attrs['disabled'] = 'disabled'


class ChainedForm(forms.Form):
    city = selectable.AutoCompleteSelectField(
        lookup_class=CityLookup,
        label='City',
        required=False,
        widget=selectable.AutoComboboxSelectWidget
    )
    state = USStateField(widget=USStateSelect, required=False)


class FarmForm(forms.ModelForm):

    class Meta(object):
        model = Farm
        widgets = {
            'fruit': selectable.AutoCompleteSelectMultipleWidget(lookup_class=FruitLookup),
        }
        fields = ('name', 'owner', 'fruit', )


FarmFormset = modelformset_factory(Farm, FarmForm)
