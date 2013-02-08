/* Test utility functions */
(function ($) {

    window.createTextComplete = function (name, attrs) {
        var inputAttrs = {
            'name': name,
            'data-selectable-type': 'text',
            'data-selectable-url': '/lookup/core-fruitlookup/',
            'type': 'text'
        }, finalAttrs = $.extend({}, inputAttrs, attrs || {});
        return $('<input>', finalAttrs);
    };

    window.createTextCombobox = function (name, attrs) {
        // Force change of the name and type
        var inputAttrs = $.extend({
            'data-selectable-type': 'combobox'
        }, attrs || {});
        return window.createTextComplete(name, inputAttrs);
    };

    window.createTextSelect = function (name, attrs) {
        var inputAttrs = $.extend({
            'name': name + '_0'
        }, attrs || {}), textInput, hiddenInput,
        hiddenAttrs = {
            'name': name + '_1',
            'data-selectable-type': 'hidden',
            'type': 'hidden'
        };
        textInput = window.createTextComplete(name, inputAttrs);
        hiddenInput = $('<input>', hiddenAttrs);
        return [textInput, hiddenInput];
    };

    window.createComboboxSelect = function (name, attrs) {
        var inputAttrs = $.extend({
            'name': name + '_0'
        }, attrs || {}), textInput, hiddenInput,
        hiddenAttrs = {
            'name': name + '_1',
            'data-selectable-type': 'hidden',
            'type': 'hidden'
        };
        textInput = window.createTextCombobox(name, inputAttrs);
        hiddenInput = $('<input>', hiddenAttrs);
        return [textInput, hiddenInput];
    };

    window.createTextSelectMultiple = function (name, attrs) {
        var inputAttrs = $.extend({
            'name': name + '_0',
            'selectable-multiple': true
        }, attrs || {}), textInput, hiddenInput,
        hiddenAttrs = {
            'name': name + '_1',
            'data-selectable-type': 'hidden-multiple',
            'type': 'hidden'
        };
        textInput = window.createTextComplete(name, inputAttrs);
        hiddenInput = $('<input>', hiddenAttrs);
        return [textInput, hiddenInput];
    };

    window.createComboboxSelectMultiple = function (name, attrs) {
        var inputAttrs = $.extend({
            'name': name + '_0',
            'selectable-multiple': true
        }, attrs || {}), textInput, hiddenInput,
        hiddenAttrs = {
            'name': name + '_1',
            'data-selectable-type': 'hidden-multiple',
            'type': 'hidden'
        };
        textInput = window.createTextCombobox(name, inputAttrs);
        hiddenInput = $('<input>', hiddenAttrs);
        return [textInput, hiddenInput];
    };
})(jQuery);