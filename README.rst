django-selectable
===================

Tools and widgets for using/creating auto-complete selection widgets using Django and jQuery UI.

.. image:: https://travis-ci.org/mlavin/django-selectable.svg?branch=master
    :target: https://travis-ci.org/mlavin/django-selectable

.. image:: https://codecov.io/github/mlavin/django-selectable/coverage.svg?branch=master
    :target: https://codecov.io/github/mlavin/django-selectable?branch=master


.. note::

    This project is looking for additional maintainers to help with Django/jQuery compatibility
    issues as well as addressing support issues/questions. If you are looking to help out
    on this project and take a look at the open
    `help-wanted <https://github.com/mlavin/django-selectable/issues?q=is%3Aissue+is%3Aopen+label%3Ahelp-wanted>`_
    or `question <https://github.com/mlavin/django-selectable/issues?q=is%3Aissue+is%3Aopen+label%3Aquestion>`_
    and see if you can contribute a fix. Be bold! If you want to take a larger role on
    the project, please reach out on the 
    `mailing list <http://groups.google.com/group/django-selectable>`_. I'm happy to work
    with you to get you going on an issue.


Features
-----------------------------------

- Works with the latest jQuery UI Autocomplete library
- Auto-discovery/registration pattern for defining lookups


Installation Requirements
-----------------------------------

- Python 2.7, 3.3+
- `Django <http://www.djangoproject.com/>`_ >= 1.7, < 1.11
- `jQuery <http://jquery.com/>`_ >= 1.9, < 3.0
- `jQuery UI <http://jqueryui.com/>`_ >= 1.10, < 1.12

To install::

    pip install django-selectable

Next add `selectable` to your `INSTALLED_APPS` to include the related css/js::

    INSTALLED_APPS = (
        'contrib.staticfiles',
        # Other apps here
        'selectable',
    )

The jQuery and jQuery UI libraries are not included in the distribution but must be included
in your templates. See the example project for an example using these libraries from the
Google CDN.

Once installed you should add the urls to your root url patterns::

    urlpatterns = [
        # Other patterns go here
        url(r'^selectable/', include('selectable.urls')),
    ]


Documentation
-----------------------------------

Documentation for django-selectable is available on `Read The Docs <http://django-selectable.readthedocs.io/en/latest/>`_.


Additional Help/Support
-----------------------------------

You can find additional help or support on the mailing list: http://groups.google.com/group/django-selectable


Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out our `contributing guide <http://readthedocs.org/docs/django-selectable/en/latest/contribute.html>`_.

If you are interested in translating django-selectable into your native language
you can join the `Transifex project <https://www.transifex.com/projects/p/django-selectable/>`_.

