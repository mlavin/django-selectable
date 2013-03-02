/*global define, module, test, expect, equal, ok*/

define(['selectable'], function ($) {

    var expectedNamespace = 'djselectable';
    if (window.uiversion.lastIndexOf('1.10', 0) === 0) {
        // jQuery UI 1.10 introduces a namespace change to include ui-prefix
        expectedNamespace = 'ui-' + expectedNamespace;
    }

    module("Autocomplete Text Methods Tests");

    test("Bind Input", function () {
        expect(2);
        var input = createTextComplete('autocomplete');
        $('#qunit-fixture').append(input);
        bindSelectables('#qunit-fixture');
        ok(input.hasClass('ui-autocomplete-input'), "input should be bound with djselecable widget");
        ok(input.data(expectedNamespace), "input should be bound with djselecable widget");
    });

    test("Manual Selection", function () {
        expect(1);
        var item = {id: "1", value: 'foo'},
            input = createTextComplete('autocomplete');
        $('#qunit-fixture').append(input);
        bindSelectables('#qunit-fixture');
        input.djselectable('select', item);
        equal(input.val(), item.value, "input should get item value");
    });

    test("Initial Data", function () {
        expect(1);
        var input = createTextComplete('autocomplete');
        input.val('Foo');
        $('#qunit-fixture').append(input);
        bindSelectables('#qunit-fixture');
        equal(input.val(), 'Foo', "initial text value should not be lost");
    });


    module("Autocombobox Text Methods Tests");

    test("Bind Input", function () {
        expect(3);
        var input = createTextCombobox('autocombobox'), button;
        $('#qunit-fixture').append(input);
        bindSelectables('#qunit-fixture');
        button = $('.ui-combo-button', '#qunit-fixture');
        ok(input.hasClass('ui-autocomplete-input'), "input should be bound with djselecable widget");
        ok(input.data(expectedNamespace), "input should be bound with djselecable widget");
        equal(button.length, 1, "combobox button should be created");
    });

    test("Manual Selection", function () {
        expect(1);
        var item = {id: "1", value: 'foo'},
            input = createTextCombobox('autocombobox');
        $('#qunit-fixture').append(input);
        bindSelectables('#qunit-fixture');
        input.djselectable('select', item);
        equal(input.val(), item.value, "input should get item value");
    });

    test("Initial Data", function () {
        expect(1);
        var input = createTextCombobox('autocombobox');
        input.val('Foo');
        $('#qunit-fixture').append(input);
        bindSelectables('#qunit-fixture');
        equal(input.val(), 'Foo', "initial text value should not be lost");
    });

    module("Autocomplete Select Methods Tests");

    test("Bind Input", function () {
        expect(2);
        var inputs = createTextSelect('autocompleteselect'),
            textInput = inputs[0], hiddenInput = inputs[1];
        $('#qunit-fixture').append(textInput);
        $('#qunit-fixture').append(hiddenInput);
        bindSelectables('#qunit-fixture');
        ok(textInput.hasClass('ui-autocomplete-input'), "input should be bound with djselecable widget");
        ok(textInput.data(expectedNamespace), "input should be bound with djselecable widget");
    });

    test("Manual Selection", function () {
        expect(2);
        var item = {id: "1", value: 'foo'},
            inputs = createTextSelect('autocompleteselect'),
            textInput = inputs[0], hiddenInput = inputs[1];
        $('#qunit-fixture').append(textInput);
        $('#qunit-fixture').append(hiddenInput);
        bindSelectables('#qunit-fixture');
        textInput.djselectable('select', item);
        equal(textInput.val(), item.value, "input should get item value");
        equal(hiddenInput.val(), item.id, "input should get item id");
    });

    test("Initial Data", function () {
        expect(2);
        var inputs = createTextSelect('autocompleteselect'),
            textInput = inputs[0], hiddenInput = inputs[1];
        $('#qunit-fixture').append(textInput);
        $('#qunit-fixture').append(hiddenInput);
        textInput.val('Foo');
        hiddenInput.val('1');
        bindSelectables('#qunit-fixture');
        equal(textInput.val(), 'Foo', "initial text value should not be lost");
        equal(hiddenInput.val(), '1', "initial pk value should not be lost");
    });

    module("Autocombobox Select Methods Tests");

    test("Bind Input", function () {
        expect(3);
        var inputs = createComboboxSelect('autocomboboxselect'),
            textInput = inputs[0], hiddenInput = inputs[1], button;
        $('#qunit-fixture').append(textInput);
        $('#qunit-fixture').append(hiddenInput);
        bindSelectables('#qunit-fixture');
        button = $('.ui-combo-button', '#qunit-fixture');
        ok(textInput.hasClass('ui-autocomplete-input'), "input should be bound with djselecable widget");
        ok(textInput.data(expectedNamespace), "input should be bound with djselecable widget");
        equal(button.length, 1, "combobox button should be created");
    });

    test("Manual Selection", function () {
        expect(2);
        var item = {id: "1", value: 'foo'},
            inputs = createComboboxSelect('autocomboboxselect'),
            textInput = inputs[0], hiddenInput = inputs[1];
        $('#qunit-fixture').append(textInput);
        $('#qunit-fixture').append(hiddenInput);
        bindSelectables('#qunit-fixture');
        textInput.djselectable('select', item);
        equal(textInput.val(), item.value, "input should get item value");
        equal(hiddenInput.val(), item.id, "input should get item id");
    });

    test("Initial Data", function () {
        expect(2);
        var inputs = createComboboxSelect('autocomboboxselect'),
            textInput = inputs[0], hiddenInput = inputs[1];
        $('#qunit-fixture').append(textInput);
        $('#qunit-fixture').append(hiddenInput);
        textInput.val('Foo');
        hiddenInput.val('1');
        bindSelectables('#qunit-fixture');
        equal(textInput.val(), 'Foo', "initial text value should not be lost");
        equal(hiddenInput.val(), '1', "initial pk value should not be lost");
    });

    module("Autocomplete Select Multiple Methods Tests");

    test("Bind Input", function () {
        expect(3);
        var inputs = createTextSelectMultiple('autocompletemultiple'),
            textInput = inputs[0], deck;
        $('#qunit-fixture').append(textInput);
        bindSelectables('#qunit-fixture');
        deck = $('.selectable-deck', '#qunit-fixture');
        ok(textInput.hasClass('ui-autocomplete-input'), "input should be bound with djselecable widget");
        ok(textInput.data(expectedNamespace), "input should be bound with djselecable widget");
        equal($('li', deck).length, 0, "no initial deck items");
    });

    test("Manual Selection", function () {
        expect(2);
        var item = {id: "1", value: 'foo'},
            inputs = createTextSelectMultiple('autocompletemultiple'),
            textInput = inputs[0], hiddenInput;
        $('#qunit-fixture').append(textInput);
        bindSelectables('#qunit-fixture');
        textInput.djselectable('select', item);
        hiddenInput = $(':input[type=hidden][name=autocompletemultiple_1]', '#qunit-fixture');
        equal(textInput.val(), '', "input should be empty");
        equal(hiddenInput.val(), item.id, "input should get item id");
    });

    test("Initial Data", function () {
        expect(3);
        var inputs = createTextSelectMultiple('autocomboboxselect'),
            textInput = inputs[0], hiddenInput = inputs[1], deck;
        $('#qunit-fixture').append(textInput);
        $('#qunit-fixture').append(hiddenInput);
        textInput.val('Foo');
        hiddenInput.val('1');
        bindSelectables('#qunit-fixture');
        deck = $('.selectable-deck', '#qunit-fixture');
        equal(textInput.val(), '', "input should be empty");
        equal(hiddenInput.val(), '1', "initial pk value should not be lost");
        equal($('li', deck).length, 1, "one initial deck items");
    });

    module("Autocombobox Select Multiple Methods Tests");

    test("Bind Input", function () {
        expect(4);
        var inputs = createComboboxSelectMultiple('autocomboboxmultiple'),
            textInput = inputs[0], deck, button;
        $('#qunit-fixture').append(textInput);
        bindSelectables('#qunit-fixture');
        deck = $('.selectable-deck', '#qunit-fixture');
        button = $('.ui-combo-button', '#qunit-fixture');
        ok(textInput.hasClass('ui-autocomplete-input'), "input should be bound with djselecable widget");
        ok(textInput.data(expectedNamespace), "input should be bound with djselecable widget");
        equal($('li', deck).length, 0, "no initial deck items");
        equal(button.length, 1, "combobox button should be created");
    });

    test("Manual Selection", function () {
        expect(2);
        var item = {id: "1", value: 'foo'},
            inputs = createComboboxSelectMultiple('autocomboboxmultiple'),
            textInput = inputs[0], hiddenInput;
        $('#qunit-fixture').append(textInput);
        bindSelectables('#qunit-fixture');
        textInput.djselectable('select', item);
        hiddenInput = $(':input[type=hidden][name=autocomboboxmultiple_1]', '#qunit-fixture');
        equal(textInput.val(), '', "input should be empty");
        equal(hiddenInput.val(), item.id, "input should get item id");
    });

    test("Initial Data", function () {
        expect(3);
        var inputs = createComboboxSelectMultiple('autocomboboxmultiple'),
            textInput = inputs[0], hiddenInput = inputs[1], deck;
        $('#qunit-fixture').append(textInput);
        $('#qunit-fixture').append(hiddenInput);
        textInput.val('Foo');
        hiddenInput.val('1');
        bindSelectables('#qunit-fixture');
        deck = $('.selectable-deck', '#qunit-fixture');
        equal(textInput.val(), '', "input should be empty");
        equal(hiddenInput.val(), '1', "initial pk value should not be lost");
        equal($('li', deck).length, 1, "one initial deck items");
    });
});