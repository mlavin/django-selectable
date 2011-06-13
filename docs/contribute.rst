.. _contributing-guide:

Contributing
==================

There are plenty of ways to contribute to this project. If you think you've found
a bug please submit an issue. If there is a feature you'd like to see then please
open an ticket proposal for it. If you've come up with some helpful examples then
you can add to our example project.


Getting the Source
--------------------------------------

The source code is hosted on `Bitbucket <https://bitbucket.org/mlavin/django-selectable>`_.
You can download the full source by cloning the hg repo::

    hg clone https://bitbucket.org/mlavin/django-selectable

Feel free to fork the project and make your own changes. If you think that it would
be helpful for other then please submit a pull request to have it merged in.


Submit an Issue
--------------------------------------

The issues are also managed on `Bitbucket <https://bitbucket.org/mlavin/django-selectable/issues>`_.
If you think you've found a bug it's helpful if you indicate the version of django-selectable
you are using the ticket version flag. If you think your bug is javascript related it is
also helpful to know the version of jQuery, jQuery UI, and the browser you are using.

Issues are also used to track new features. If you have a feature you would like to see
you can submit a proposal ticket. You can also see features which are planned here.


Running the Test Suite
--------------------------------------

There are a number of tests in place to test the server side code for this
project. To run the tests you need Django installed and run::

    python selectable/tests/runtests.py

Tests for the client side code is planned. If javascript testing is something you
are familiar with then it would be a great help to this project.


Building the Documentation
--------------------------------------

The documentation is built using `Sphinx <http://sphinx.pocoo.org/>`_ 
and available on `Read the Docs <http://django-selectable.readthedocs.org/>`_. With
Sphinx installed you can build the documentation by running::

    make html

inside the docs directory. Documentation fixes and improvements are always welcome.

