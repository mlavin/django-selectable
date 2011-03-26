from django.contrib import admin
from django import forms

import selectable.forms as selectable

from example.core.models import Fruit, Farm
from example.core.lookups import FruitLookup, OwnerLookup


class FarmAdminForm(forms.ModelForm):
    owner = selectable.AutoComboboxSelectField(lookup_class=OwnerLookup)
    fruit = selectable.AutoCompleteSelectMultipleField(lookup_class=FruitLookup)

    class Meta(object):
        model = Farm


class FarmAdmin(admin.ModelAdmin):
    form = FarmAdminForm


admin.site.register(Fruit)
admin.site.register(Farm, FarmAdmin)
