Admin Integration
====================

Overview
--------------------------------------

Django-Selectables will work in the admin. To get started on integrated the
fields and widgets in the admin make sure you are familiar with the Django
documentation on the `ModelAdmin.form <http://docs.djangoproject.com/en/1.3/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form>`_ 
and `ModelForms <http://docs.djangoproject.com/en/1.3/topics/forms/modelforms/>`_ particularly
on `overriding the default widgets <http://docs.djangoproject.com/en/1.3/topics/forms/modelforms/#overriding-the-default-field-types-or-widgets>`_. As you will see integrating Django-Selectables in the admin
is the same as working with regular forms.


Basic Example
--------------------------------------

In our sample project we have a `Farm` model with a foreign key to `auth.User` and 
a many to many relation to our `Fruit` model.

    .. literalinclude:: ../example/core/models.py
        :lines: 11-17

In `admin.py` we will define the form and associate it with the `FarmAdmin`.

    .. literalinclude:: ../example/core/admin.py
        :lines: 12-36

You'll note this form also for new users to be created and associated with the
farm if no user is found matching the given name. To make use of this feature we
need to add `owner` to the exclude so that it will pass model validation. Unfortunately
that means we must set the owner manual in the save and in the initial data because
the `ModelForm` will no longer do this for you. Since `fruit` does not allow new
items you'll see these steps are not necessary.


Inline Example
--------------------------------------

With our `Farm` model we can also associate the `UserAdmin` with a `Farm`
by making use of the `InlineModelAdmin 
<http://docs.djangoproject.com/en/1.3/ref/contrib/admin/#inlinemodeladmin-objects>`_.
We can even make use of the same `FarmAdminForm`.

    .. literalinclude:: ../example/core/admin.py
        :lines: 39-48

The auto-complete functions will be bound as new forms are added dynamically.

