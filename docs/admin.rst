Admin Integration
====================

Overview
--------------------------------------

Django-Selectables will work in the admin. To get started on integrated the
fields and widgets in the admin make sure you are familiar with the Django
documentation on the `ModelAdmin.form <http://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form>`_
and `ModelForms <http://docs.djangoproject.com/en/stable/topics/forms/modelforms/>`_ particularly
on `overriding the default widgets <http://docs.djangoproject.com/en/stable/topics/forms/modelforms/#overriding-the-default-field-types-or-widgets>`_.
As you will see integrating django-selectable in the adminis the same as working with regular forms.


.. _admin-jquery-include:

Including jQuery & jQuery UI
--------------------------------------

As noted :ref:`in the quick start guide <start-include-jquery>`, the jQuery and jQuery UI libraries
are not included in the distribution but must be included in your templates. For the
Django admin that means overriding
`admin/base_site.html <https://code.djangoproject.com/browser/django/trunk/django/contrib/admin/templates/admin/base_site.html>`_.
You can include this media in the block name `extrahead` which is defined in
`admin/base.html <https://code.djangoproject.com/browser/django/trunk/django/contrib/admin/templates/admin/base.html>`_.

    .. code-block:: html

        {% block extrahead %}
            {% load selectable_tags %}
            {% include_ui_theme %}
            {% include_jquery_libs %}
            {{ block.super }}
        {% endblock %}

See the Django documentation on
`overriding admin templates <https://docs.djangoproject.com/en/stable/ref/contrib/admin/#overriding-admin-templates>`_.
See the example project for the full template example.


.. _admin-grappelli:

Using Grappelli
--------------------------------------

`Grappelli <https://django-grappelli.readthedocs.org>`_ is a popular customization of the Django
admin interface. It includes a number of interface improvements which are also built on top of
jQuery UI. When using Grappelli you do not need to make any changes to the ``admin/base_site.html``
template. django-selectable will detect jQuery and jQuery UI versions included by Grappelli
and make use of them.


.. _admin-basic-example:

Basic Example
--------------------------------------

For example, we may have a ``Farm`` model with a foreign key to ``auth.User`` and
a many to many relation to our ``Fruit`` model.

    .. code-block:: python

        from __future__ import unicode_literals

        from django.db import models
        from django.utils.encoding import python_2_unicode_compatible


        @python_2_unicode_compatible
        class Fruit(models.Model):
            name = models.CharField(max_length=200)

            def __str__(self):
                return self.name


        @python_2_unicode_compatible
        class Farm(models.Model):
            name = models.CharField(max_length=200)
            owner = models.ForeignKey('auth.User', related_name='farms')
            fruit = models.ManyToManyField(Fruit)

            def __str__(self):
                return "%s's Farm: %s" % (self.owner.username, self.name)

In `admin.py` we will define the form and associate it with the `FarmAdmin`.

    .. code-block:: python

        from django.contrib import admin
        from django.contrib.auth.admin import UserAdmin
        from django.contrib.auth.models import User
        from django import forms

        from selectable.forms import AutoCompleteSelectField, AutoCompleteSelectMultipleWidget

        from .models import Fruit, Farm
        from .lookups import FruitLookup, OwnerLookup


        class FarmAdminForm(forms.ModelForm):
            owner = AutoCompleteSelectField(lookup_class=OwnerLookup, allow_new=True)

            class Meta(object):
                model = Farm
                widgets = {
                    'fruit': AutoCompleteSelectMultipleWidget(lookup_class=FruitLookup),
                }
                exclude = ('owner', )

            def __init__(self, *args, **kwargs):
                super(FarmAdminForm, self).__init__(*args, **kwargs)
                if self.instance and self.instance.pk and self.instance.owner:
                    self.initial['owner'] = self.instance.owner.pk

            def save(self, *args, **kwargs):
                owner = self.cleaned_data['owner']
                if owner and not owner.pk:
                    owner = User.objects.create_user(username=owner.username, email='')
                self.instance.owner = owner
                return super(FarmAdminForm, self).save(*args, **kwargs)


        class FarmAdmin(admin.ModelAdmin):
            form = FarmAdminForm


        admin.site.register(Farm, FarmAdmin)


You'll note this form also allows new users to be created and associated with the
farm, if no user is found matching the given name. To make use of this feature we
need to add ``owner`` to the exclude so that it will pass model validation. Unfortunately
that means we must set the owner manual in the save and in the initial data because
the ``ModelForm`` will no longer do this for you. Since ``fruit`` does not allow new
items you'll see these steps are not necessary.

The django-selectable widgets are compatitible with the add another popup in the
admin. It's that little green plus sign that appears next to ``ForeignKey`` or
``ManyToManyField`` items. This makes django-selectable a user friendly replacement
for the `ModelAdmin.raw_id_fields <https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.raw_id_fields>`_
when the default select box grows too long.


.. _admin-inline-example:

Inline Example
--------------------------------------

With our ``Farm`` model we can also associate the ``UserAdmin`` with a ``Farm``
by making use of the `InlineModelAdmin
<http://docs.djangoproject.com/en/stable/ref/contrib/admin/#inlinemodeladmin-objects>`_.
We can even make use of the same ``FarmAdminForm``.

    .. code-block:: python

        # continued from above

        class FarmInline(admin.TabularInline):
            model = Farm
            form = FarmAdminForm


        class NewUserAdmin(UserAdmin):
            inlines = [
                FarmInline,
            ]


        admin.site.unregister(User)
        admin.site.register(User, NewUserAdmin)

The auto-complete functions will be bound as new forms are added dynamically.

