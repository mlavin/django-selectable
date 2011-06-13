Overview
==================

Motivation
--------------------------------------

There are many Django apps related to auto-completion why create another? One problem
was varying support for the `jQuery UI auto-complete plugin <http://jqueryui.com/demos/autocomplete/>`_ 
versus the now deprecated `bassistance version <http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete/>`_.
Another was support for combo-boxes and multiple selects. And lastly was a simple syntax for
defining the related backend views for the auto-completion.

This library aims to meet all of these goals:
    - Built on jQuery UI auto-complete
    - Fields and widgets for a variety of use-cases:
        - Text inputs and combo-boxes
        - Text selection
        - Value/ID/Foreign key selection
        - Multiple object selection
        - Allowing new values
    - Simple and extendable syntax for defining backend views


Related Projects
--------------------------------------

Much of the work here was inspired by things that I like (and things I don't like) about
`django-ajax-selects <http://code.google.com/p/django-ajax-selects/>`_. To see some of the
other Django apps for handling auto-completion see `Django-Packages <http://djangopackages.com/grids/g/auto-complete/>`_.
