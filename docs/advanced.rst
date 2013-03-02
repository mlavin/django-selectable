Advanced Usage
==========================

We've gone through the most command and simple use cases for django-selectable. Now
we'll take a lot at some of the more advanced features of this project. This assumes
that you are comfortable reading and writing a little bit of Javascript making
use of jQuery.


.. _additional-parameters:

Additional Parameters
--------------------------------------

The basic lookup is based on handling a search based on a single term string.
If additional filtering is needed it can be inside the lookup ``get_query`` but
you would need to define this when the lookup is defined. While this fits a fair
number of use cases there are times when you need to define additional query
parameters that won't be know until the either the form is bound or until selections
are made on the client side. This section will detail how to handle both of these
cases.


How Parameters are Passed
_______________________________________

As with the search term the additional parameters you define will be passed in
``request.GET``. Since ``get_query`` gets the current request so you will have access to
them. Since they can be manipulated on the client side, these parameters should be
treated like all user input. It should be properly validated and sanitized.


Limiting the Result Set
_______________________________________

The number of results are globally limited/paginated by the :ref:`SELECTABLE_MAX_LIMIT`
but you can also lower this limit on the field or widget level. Each field and widget
takes a ``limit`` argument in the ``__init__`` that will be passed back to the lookup
through the ``limit`` query parameter. The result set will be automatically paginated
for you if you use either this parameter or the global setting.


.. _server-side-parameters:

Adding Parameters on the Server Side
_______________________________________

Each of the widgets define ``update_query_parameters`` which takes a dictionary. The
most common way to use this would be in the form ``__init__``.

    .. code-block:: python

        class FruitForm(forms.Form):
            autocomplete = forms.CharField(
                label='Type the name of a fruit (AutoCompleteWidget)',
                widget=selectable.AutoCompleteWidget(FruitLookup),
                required=False,
            )

            def __init__(self, *args, **kwargs):
                super(FruitForm, self).__init__(*args, **kwargs)
                self.fields['autocomplete'].widget.update_query_parameters({'foo': 'bar'})

You can also pass the query parameters into the widget using the ``query_params``
keyword argument. It depends on your use case as to whether the parameters are
know when the form is defined or when an instance of the form is created.


.. _client-side-parameters:

Adding Parameters on the Client Side
_______________________________________

There are times where you want to filter the result set based other selections
by the user such as a filtering cities by a previously selected state. In this
case you will need to bind a ``prepareQuery`` to the field. This function should accept the query dictionary.
You are free to make adjustments to  the query dictionary as needed.

    .. code-block:: html

        <script type="text/javascript">
            function newParameters(query) {
                query.foo = 'bar';
            }

            $(document).ready(function() {
                $('#id_autocomplete').djselectable('option', 'prepareQuery', newParameters);
            });
        </script>

.. note::

    In v0.7 the scope of ``prepareQuery`` was updated so that ``this`` refers to the
    current ``djselectable`` plugin instance. Previously ``this`` refered to the
    plugin ``options`` instance.


.. _chain-select-example:

Chained Selection
--------------------------------------

It's a fairly common pattern to have two or more inputs depend one another such City/State/Zip.
In fact there are other Django apps dedicated to this purpose such as
`django-smart-selects <https://github.com/digi604/django-smart-selects>`_ or
`django-ajax-filtered-fields <http://code.google.com/p/django-ajax-filtered-fields/>`_.
It's possible to handle this kind of selection with django-selectable if you are willing
to write a little javascript.

Suppose we have city model

    .. literalinclude:: ../example/core/models.py
        :pyobject: City

and a simple form

    .. literalinclude:: ../example/core/forms.py
        :pyobject: ChainedForm

We want our users to select a city and if they choose a state then we will only
show them cities in that state. To do this we will pass back chosen state as
addition parameter with the following javascript:

    .. literalinclude:: ../example/core/templates/advanced.html
        :language: html
        :start-after: {% block extra-js %}
        :end-before: {% endblock %}


Then in our lookup we will grab the state value and filter our results on it:

    .. literalinclude:: ../example/core/lookups.py
        :pyobject: CityLookup

And that's it! We now have a working chained selection example. The full source
is included in the example project.

.. _client-side-changes:

Detecting Client Side Changes
____________________________________________

The previous example detected selection changes on the client side to allow passing
parameters to the lookup. Since django-selectable is built on top of the jQuery UI
`Autocomplete plug-in <http://jqueryui.com/demos/autocomplete/>`_, the widgets
expose the events defined by the plugin.

    - djselectablecreate
    - djselectablesearch
    - djselectableopen
    - djselectablefocus
    - djselectableselect
    - djselectableclose
    - djselectablechange

.. note::

    Prior to v0.7 these event names were under the ``autocomplete`` namespace. If you
    are upgrading from a previous version and had customizations using these events
    you should be sure to update the names.

For the most part these event names should be self-explanatory. If you need additional
detail you should refer to the `jQuery UI docs on these events <http://jqueryui.com/demos/autocomplete/#events>`_.

The multiple select widgets include additional events which indicate when a new item is added
or removed from the current list. These events are ``djselectableadd`` and ``djselectableremove``.
These events pass a dictionary of data with the following keys

    - element: The original text input
    - input: The hidden input to be added for the new item
    - wrapper: The ``<li>`` element to be added to the deck
    - deck: The outer ``<ul>`` deck element

You can use these events to prevent items from being added or removed from the deck by
returning ``false`` in the handling function. A simple example is given below:

    .. code-block:: html

        <script type="text/javascript">
            $(document).ready(function() {
                $(':input[name=my_field_0]').bind('djselectableadd', function(event, item) {
                    // Don't allow foo to be added
                    if ($(item.input).val() === 'foo') {
                        return false;
                    }
                });
            });
        </script>


Submit On Selection
--------------------------------------

You might want to help your users by submitting the form once they have selected a valid
item. To do this you simply need to listen for the ``djselectableselect`` event. This
event is fired by the text input which has an index of 0. If your field is named ``my_field``
then input to watch would be ``my_field_0`` such as:

    .. code-block:: html

        <script type="text/javascript">
            $(document).ready(function() {
                $(':input[name=my_field_0]').bind('djselectableselect', function(event, ui) {
                    $(this).parents("form").submit();
                });
            });
        </script>


Dynamically Added Forms
--------------------------------------

django-selectable can work with dynamically added forms such as inlines in the admin.
To make django-selectable work in the admin there is nothing more to do than include
the necessary static media as described in the
:ref:`Admin Integration <admin-jquery-include>` section.

If you are making use of the popular `django-dynamic-formset <http://code.google.com/p/django-dynamic-formset/>`_
then you can make django-selectable work by passing ``bindSelectables`` to the
`added <http://code.google.com/p/django-dynamic-formset/source/browse/trunk/docs/usage.txt#259>`_ option:

    .. code-block:: html

        <script type="text/javascript">
            $(document).ready(function() {
                $('#my-formset').formset({
               		added: bindSelectables
                });
            });
        </script>

Currently you must include the django-selectable javascript below this formset initialization
code for this to work. See django-selectable `issue #31 <https://bitbucket.org/mlavin/django-selectable/issue/31/>`_
for some additional detail on this problem.


.. _advanced-label-formats:

Label Formats on the Client Side
--------------------------------------

The lookup label is the text which is shown in the list before it is selected.
You can use the :ref:`get_item_label <lookup-get-item-label>` method in your lookup
to do this on the server side. This works for most applications. However if you don't
want to write your HTML in Python or need to adapt the format on the client side you
can use the :ref:`formatLabel <javascript-formatLabel>` option.

``formatLabel`` takes two paramaters the current label and the current selected item.
The item is a dictionary object matching what is returned by the lookup's
:ref:`format_item <lookup-format-item>`. ``formatLabel`` should return the string
which should be used for the label.

.. note::

    In v0.7 the scope of ``formatLabel`` was updated so that ``this`` refers to the
    current ``djselectable`` plugin instance. Previously ``this`` refered to the
    plugin ``options`` instance.

Going back to the ``CityLookup`` we can adjust the label to wrap the city and state
portions with their own classes for additional styling:

    .. literalinclude:: ../example/core/lookups.py
        :pyobject: CityLookup

    .. code-block:: html

        <script type="text/javascript">
            $(document).ready(function() {
                function formatLabel(label, item) {
                    var data = label.split(',');
                    return '<span class="city">' + data[0] + '</span>, <span class="state">' + data[1] + '</span>';
                }
                $('#id_city_0').djselectable('option', 'formatLabel', formatLabel);
            });
        </script>

This is a rather simple example but you could also pass additional information in ``format_item``
such as a flag of whether the city is the capital and render the state captials differently.

.. _advanced-bootstrap:

Using with Twitter Bootstrap
--------------------------------------

django-selectable can work along side with Twitter Bootstrap but there are a few things to
take into consideration. Both jQuery UI and Bootstrap define a ``$.button`` plugin. This
plugin is used by default by django-selectable and expects the UI version. If the jQuery UI
JS is included after the Bootstrap JS then this will work just fine but the Bootstrap
button JS will not be available. This is the strategy taken by the  `jQuery UI Bootstrap
<http://addyosmani.github.com/jquery-ui-bootstrap/>`_ theme.

Another option is to rename the Bootstrap plugin using the ``noConflict`` option.

    .. code-block:: html

        <!-- Include Bootstrap JS -->
        <script>$.fn.bootstrapBtn = $.fn.button.noConflict();</script>
        <!-- Include jQuery UI JS -->

Even with this some might complain that it's too resource heavy to include all of
jQuery UI when you just want the autocomplete to work with django-selectable. For
this you can use the `Download Builder <http://jqueryui.com/download/>`_ to build
a minimal set of jQuery UI widgets. django-selectable requires the UI core, autocomplete,
menu and button widgets. None of the effects or interactions are needed. Minified
this totals around 100 kb of JS, CSS and images (based on jQuery UI 1.10).

.. note::

    For a comparison this is smaller than the minified Bootstrap 2.3.0 CSS
    which is 105 kb not including the responsive CSS or the icon graphics.

It is possible to remove the dependency on the UI button plugin and instead
use the Bootstrap button styles. This is done by overriding
the ``_comboButtonTemplate`` and ``_removeButtonTemplate`` functions used to
create the buttons. An example is given below.

    .. code-block:: html

        <script>
            $.ui.djselectable.prototype._comboButtonTemplate = function (input) {
                var icon = $("<i>").addClass("icon-chevron-down");
                // Remove current classes on the text input
                $(input).attr("class", "");
                // Wrap with input-append
                $(input).wrap('<div class="input-append" />');
                // Return button link with the chosen icon
                return $("<a>").append(icon).addClass("btn btn-small");
            };
            $.ui.djselectable.prototype._removeButtonTemplate = function (item) {
                var icon = $("<i>").addClass("icon-remove-sign");
                // Return button link with the chosen icon
                return $("<a>").append(icon).addClass("btn btn-small pull-right");
            };
        </script>