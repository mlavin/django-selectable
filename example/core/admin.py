from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

import selectable.forms as selectable

from example.core.models import Fruit, Farm
from example.core.lookups import FruitLookup, OwnerLookup


class FarmAdminForm(forms.ModelForm):
    owner = selectable.AutoComboboxSelectField(lookup_class=OwnerLookup, allow_new=True)
    fruit = selectable.AutoCompleteSelectMultipleField(lookup_class=FruitLookup)

    class Meta(object):
        model = Farm

    def clean(self, *args, **kwargs):
        owner = self.cleaned_data['owner']
        if owner and not owner.pk:
            owner = User.objects.create_user(username=owner.username, email='')
            self.cleaned_data['owner'] = owner
        return self.cleaned_data
        

class FarmAdmin(admin.ModelAdmin):
    form = FarmAdminForm


admin.site.register(Fruit)
admin.site.register(Farm, FarmAdmin)
