Admin Integration
====================

Overview
--------------------------------------

Django-Selectables will work in the admin. To get started on integrated the
fields and widgets in the admin make sure you are familiar with the Django
documentation on the `ModelAdmin.form <http://docs.djangoproject.com/en/1.3/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form>`_
and `ModelForms <http://docs.djangoproject.com/en/1.3/topics/forms/modelforms/>`_ particularly
on `overriding the default widgets <http://docs.djangoproject.com/en/1.3/topics/forms/modelforms/#overriding-the-default-field-types-or-widgets>`_.
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

    .. literalinclude:: ../example/example/templates/admin/base_site.html
        :start-after: {% endblock title %}
        :end-before: {% block branding %}

See the Django documentation on
`overriding admin templates <https://docs.djangoproject.com/en/1.3/ref/contrib/admin/#overriding-admin-templates>`_.
See the example project for the full template example.


.. _admin-grappelli:

Using Grappelli
--------------------------------------

.. versionadded:: 0.7

`Grappelli <https://django-grappelli.readthedocs.org>`_ is a popular customization of the Django
admin interface. It includes a number of interface improvements which are also built on top of
jQuery UI. When using Grappelli you do not need to make any changes to the ``admin/base_site.html``
template. django-selectable will detect jQuery and jQuery UI versions included by Grappelli
and make use of them.


.. _admin-basic-example:

Basic Example
--------------------------------------

In our sample project we have a ``Farm`` model with a foreign key to ``auth.User`` and
a many to many relation to our ``Fruit`` model.

    .. literalinclude:: ../example/core/models.py
       :pyobject: Farm

In `admin.py` we will define the form and associate it with the `FarmAdmin`.

    .. literalinclude:: ../example/core/admin.py
        :pyobject: FarmAdminForm

    .. literalinclude:: ../example/core/admin.py
        :pyobject: FarmAdmin

You'll note this form also allows new users to be created and associated with the
farm, if no user is found matching the given name. To make use of this feature we
need to add ``owner`` to the exclude so that it will pass model validation. Unfortunately
that means we must set the owner manual in the save and in the initial data because
the ``ModelForm`` will no longer do this for you. Since ``fruit`` does not allow new
items you'll see these steps are not necessary.

The django-selectable widgets are compatitible with the add another popup in the
admin. It's that little green plus sign that appears next to ``ForeignKey`` or
``ManyToManyField`` items. This makes django-selectable a user friendly replacement
for the `ModelAdmin.raw_id_fields <https://docs.djangoproject.com/en/1.3/ref/contrib/admin/#django.contrib.admin.ModelAdmin.raw_id_fields>`_
when the default select box grows too long.


.. _admin-inline-example:

Inline Example
--------------------------------------

With our ``Farm`` model we can also associate the ``UserAdmin`` with a ``Farm``
by making use of the `InlineModelAdmin
<http://docs.djangoproject.com/en/1.3/ref/contrib/admin/#inlinemodeladmin-objects>`_.
We can even make use of the same ``FarmAdminForm``.

    .. literalinclude:: ../example/core/admin.py
        :pyobject: FarmInline
    .. literalinclude:: ../example/core/admin.py
        :pyobject: NewUserAdmin

The auto-complete functions will be bound as new forms are added dynamically.

