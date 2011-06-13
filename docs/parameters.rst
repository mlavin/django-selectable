Additional Parameters
=========================

The basic lookup is based on handling a search based on a single term string.
If additional filtering is needed it can be inside the lookup `get_query` but
you would need to define this when the lookup is defined. While this fits a fair
number of use cases there are times when you need to define additional query
parameters that won't be know until the either the form is bound or until selections
are made on the client side. This section will detail how to handle both of these
cases.


How Parameters are Passed
--------------------------------------

As with the search term the additional parameters you define will be passed in
`request.GET`. Since `get_query` gets the current request so you will have access to
them. Since they can be manipulated on the client side, these parameters should be
treated like all user input. It should be properly validated and sanitized.


Limiting the Result Set
--------------------------------------

The number of results are globally limited/paginated by the :ref:`SELECTABLE_MAX_LIMIT`
but you can also lower this limit on the field or widget level. Each field and widget
takes a `limit` argument in the `__init__` that will be passed back to the lookup
through the `limit` query parameter. The result set will be automatically paginated
for you if you use either this parameter or the global setting.


.. _server-side-parameters:

Adding Parameters on the Server Side
--------------------------------------

Each of the widgets define `update_query_parameters` which takes a dictionary. The
most common way to use this would be in the form `__init__`.

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


.. _client-side-parameters:

Adding Parameters on the Client Side
--------------------------------------

There are times where you want to filter the result set based other selections
by the user such as a filtering cities by a previously selected state. In this
case you will need to bind a `prepareQuery` to the field. This function should accept the query dictionary. 
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


.. _client-side-changes:

Detecting Client Side Changes
--------------------------------------

Since django-selectable is built on top of the jQuery UI 
`Autocomplete plug-in <http://jqueryui.com/demos/autocomplete/>`_, the widgets
expose the events defined by the plugin.

    - autocompletecreate
    - autocompletesearch
    - autocompleteopen
    - autocompletefocus
    - autocompleteselect
    - autocompleteclose
    - autocompletechange

For the most part these event names should be self-explanatory. If you need additional
detail you should refer to the `jQuery UI docs on these events <http://jqueryui.com/demos/autocomplete/#events>`_.

