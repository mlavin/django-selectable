/*global define, module, test, expect, equal, ok*/

define(['selectable'], function ($) {

    module("Basic Event Tests", {
        setup: function () {
            // Patch AJAX requests
            var self = this;
            this.xhr = sinon.useFakeXMLHttpRequest();
            this.requests = [];
            this.xhr.onCreate = function (xhr) {
                self.requests.push(xhr);
            };
            this.inputs = createTextSelect('autocompleteselect');
            this.textInput = this.inputs[0];
            this.hiddenInput = this.inputs[1];
            $('#qunit-fixture').append(this.textInput);
            $('#qunit-fixture').append(this.hiddenInput);
            bindSelectables('#qunit-fixture');
        },
        teardown: function () {
            this.xhr.restore();
            this.textInput.djselectable('destroy');
        }
    });

    test("Manual Selection", function() {
        expect(1);
        var count = 0,
            item = {id: "1", value: 'foo'};
        this.textInput.bind('djselectableselect', function(e, item) {
            count = count + 1;
        });
        var item = {id: "1", value: 'foo'};
        this.textInput.djselectable('select', item);
        equal(count, 1, "djselectableselect should fire once when manually selected.");
    });

    test("Manual Selection with Double Bind", function() {
        expect(1);
        var count = 0,
            item = {id: "1", value: 'foo'};
        bindSelectables('#qunit-fixture');
        this.textInput.bind('djselectableselect', function(e, item) {
            count = count + 1;
        });
        this.textInput.djselectable('select', item);
        equal(count, 1, "djselectableselect should fire once when manually selected.");
    });

    test("Menu Selection", function() {
        expect(2);
        var count = 0,
            down = jQuery.Event("keydown"),
            enter = jQuery.Event("keydown"),
            response = simpleLookupResponse(),
            self = this;
        down.keyCode = $.ui.keyCode.DOWN;
        enter.keyCode = $.ui.keyCode.ENTER;
        this.textInput.bind('djselectableselect', function(e, item) {
            count = count + 1;
        });
        this.textInput.val("ap").keydown();
        stop();
        setTimeout(function () {
            equal(self.requests.length, 1, "AJAX request should be triggered.");
            self.requests[0].respond(200, {"Content-Type": "application/json"},
                JSON.stringify(response)
            );
            self.textInput.trigger(down);
            self.textInput.trigger(enter);
            equal(count, 1, "djselectableselect should only fire once.");
            start();
        }, 300);
    });

    test("Pagination Click", function() {
        expect(3);
        var count = 0,
            response = paginatedLookupResponse(),
            self = this;
        this.textInput.bind('djselectableselect', function(e, item) {
            count = count + 1;
        });
        this.textInput.val("ap").keydown();
        stop();
        setTimeout(function () {
            equal(self.requests.length, 1, "AJAX request should be triggered.");
            self.requests[0].respond(200, {"Content-Type": "application/json"},
                JSON.stringify(response)
            );
            $('.ui-menu-item.selectable-paginator:visible a').trigger("mouseenter");
            $('.ui-menu-item.selectable-paginator:visible a').trigger("click");
            equal(self.requests.length, 2, "Another AJAX request should be triggered.");
            equal(count, 0, "djselectableselect should not fire for new page.");
            start();
        }, 300);
    });

    test("Pagination Enter", function() {
        expect(3);
        var count = 0,
            down = jQuery.Event("keydown"),
            enter = jQuery.Event("keydown"),
            response = paginatedLookupResponse(),
            self = this;
        down.keyCode = $.ui.keyCode.DOWN;
        enter.keyCode = $.ui.keyCode.ENTER;
        this.textInput.bind('djselectableselect', function(e, item) {
            count = count + 1;
        });
        this.textInput.val("ap").keydown();
        stop();
        setTimeout(function () {
            equal(self.requests.length, 1, "AJAX request should be triggered.");
            self.requests[0].respond(200, {"Content-Type": "application/json"},
                JSON.stringify(response)
            );
            self.textInput.trigger(down);
            self.textInput.trigger(down);
            self.textInput.trigger(down);
            self.textInput.trigger(enter);
            equal(self.requests.length, 2, "Another AJAX request should be triggered.");
            equal(count, 0, "djselectableselect should not fire for new page.");
            start();
        }, 300);
    });

    test("Pagination Render", function() {
        expect(2);
        var count = 0,
            down = jQuery.Event("keydown"),
            enter = jQuery.Event("keydown"),
            response = paginatedLookupResponse(),
            self = this;
        down.keyCode = $.ui.keyCode.DOWN;
        enter.keyCode = $.ui.keyCode.ENTER;
        this.textInput.val("ap").keydown();
        stop();
        setTimeout(function () {
            var options;
            self.requests[0].respond(200, {"Content-Type": "application/json"},
                JSON.stringify(response)
            );
            options = $('li.ui-menu-item:visible');
            equal(options.length, 3, "Currently 3 menu items.");
            // $('.selectable-paginator:visible').click();
            self.textInput.trigger(down);
            self.textInput.trigger(down);
            self.textInput.trigger(down);
            self.textInput.trigger(enter);
            self.requests[1].respond(200, {"Content-Type": "application/json"},
                JSON.stringify(response)
            );
            options = $('li.ui-menu-item:visible');
            equal(options.length, 5, "Now 5 menu items.");
            start();
        }, 300);
    });

    module("Custom Event Tests", {
        setup: function () {
            this.inputs = createTextSelectMultiple('autocompleteselectmultiple');
            this.textInput = this.inputs[0];
            this.hiddenInput = this.inputs[1];
            $('#qunit-fixture').append(this.textInput);
            bindSelectables('#qunit-fixture');
        }
    });

    test("Add Deck Item", function() {
        expect(1);
        var count = 0,
            item = {id: "1", value: 'foo'};
        this.textInput.bind('djselectableadd', function(e, item) {
            count = count + 1;
        });
        this.textInput.djselectable('select', item);
        equal(count, 1, "djselectableadd should fire once when manually selected.");
    });

    test("Prevent Add Deck Item", function() {
        expect(1);
        var count = 0,
            item = {id: "1", value: 'foo'},
            deck = $('.selectable-deck', '#qunit-fixture');
        this.textInput.bind('djselectableadd', function(e, item) {
            return false;
        });
        this.textInput.djselectable('select', item);
        deck = $('.selectable-deck', '#qunit-fixture');
        equal($('li', deck).length, 0, "Item should not be added.");
    });

    test("Remove Deck Item", function() {
        expect(1);
        var count = 0,
            item = {id: "1", value: 'foo'},
            deck = $('.selectable-deck', '#qunit-fixture');
        this.textInput.bind('djselectableremove', function(e, item) {
            count = count + 1;
        });
        this.textInput.djselectable('select', item);
        $('.selectable-deck-remove', deck).click();
        equal(count, 1, "djselectableremove should fire once when item is removed.");
    });

    test("Prevent Remove Deck Item", function() {
        expect(1);
        var count = 0,
            item = {id: "1", value: 'foo'},
            deck = $('.selectable-deck', '#qunit-fixture');
        this.textInput.bind('djselectableremove', function(e, item) {
            return false;
        });
        var item = {id: "1", value: 'foo'};
        this.textInput.djselectable('select', item);
        $('.selectable-deck-remove', deck).click();
        equal($('li', deck).length, 1, "Item should not be removed.");
    });
});