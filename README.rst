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
- `jQuery <http://jquery.com/>`_ >= 1.4.3
- `jQuery UI <http://jqueryui.com/>`_ >= 1.8

Optional (but recommended)

- `django-staticfiles <https://github.com/jezdez/django-staticfiles>`_

To install::
    
    pip install django-selectable

If you are using `django-staticfiles` (or `django.contrib.staticfiles` in Django 1.3) then
add `selectable` to your `INSTALLED_APPS` to include the related css/js.

The jQuery and jQuery UI libraries are not included in the distribution but must be included
in your templates. See the example project for an example using these libraries from the
Google CDN.

Once installed you should add the urls to your root url patterns::

        urlpatterns = patterns('',
            # Other patterns go here
            (r'^selectable/', include('selectable.urls')),
        )


Documentation
-----------------------------------

Documentation for django-selectable is available on 
`Read The Docs <http://readthedocs.org/>`_:

- `Dev <http://readthedocs.org/docs/django-selectable/en/latest/>`_
- `v0.4.0 <http://readthedocs.org/docs/django-selectable/en/version-0.4.0/>`_
- `v0.3.1 <http://readthedocs.org/docs/django-selectable/en/version-0.3.1/>`_
- `v0.2.0 <http://readthedocs.org/docs/django-selectable/en/version-0.2.0/>`_
- `v0.1.2 <http://readthedocs.org/docs/django-selectable/en/version-0.1.2/>`_


Additional Help/Support
-----------------------------------

You can find additional help or support on the mailing list: http://groups.google.com/group/django-selectable


Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out our `contributing guide <http://readthedocs.org/docs/django-selectable/en/latest/contribute.html>`_.

