from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

import selectable.forms as selectable
from selectable.forms.widgets import MEDIA_PREFIX

from example.core.models import Fruit, Farm
from example.core.lookups import FruitLookup, OwnerLookup


class FarmAdminForm(forms.ModelForm):
    owner = selectable.AutoComboboxSelectField(lookup_class=OwnerLookup, allow_new=True)

    class Meta(object):
        model = Farm
        widgets = {
            'fruit': selectable.AutoCompleteSelectMultipleWidget(lookup_class=FruitLookup),
        }

    def clean(self, *args, **kwargs):
        owner = self.cleaned_data['owner']
        if owner and not owner.pk:
            owner = User.objects.create_user(username=owner.username, email='')
            self.cleaned_data['owner'] = owner
        return self.cleaned_data


class FarmAdmin(admin.ModelAdmin):
    form = FarmAdminForm


class FarmInline(admin.TabularInline):
    model = Farm
    form = FarmAdminForm

    class Media(object):
        js = ('%sjs/inlines.js' % MEDIA_PREFIX, )


class NewUserAdmin(UserAdmin):
    inlines = [
        FarmInline,
    ]


admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
admin.site.register(Fruit)
admin.site.register(Farm, FarmAdmin)
