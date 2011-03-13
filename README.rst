django-selectable
===================

Tools and widgets for using/creating auto-complete selection widgets using Django and jQuery UI.

Features
-----------------------------------

- Works with the latest jQuery UI Autocomplete library
- Auto-discovery/registration pattern for defining lookups


Installation Requirements
-----------------------------------

- `Django <http://www.djangoproject.com/>`_ >= 1.2
- `jQuery <http://jquery.com/>`_ >= 1.4
- `jQuery UI <http://jqueryui.com/>`_ >= 1.8

Optional (but recommended)

- `django-staticfiles <https://github.com/jezdez/django-staticfiles>`_

To install::
    
    pip install django-selectable

If you are using `django-staticfiles` (or `django.contrib.staticfiles` in Django 1.3) then
add `selectable` to your `INSTALLED_APPS` to include the related css/js.

The jQuery and jQuery UI libraries are not included in the distribution but should be included
in your templates. See the example project for an example using these libraries from the
Google CDN.

