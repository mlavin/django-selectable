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

    asyncTest("Menu Selection", function() {
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
        setTimeout(function () {
            equal(self.requests.length, 1, "AJAX request should be triggered.");
            self.requests[0].respond(200, {"Content-Type": "application/json"},
                JSON.stringify(response)
            );
            self.textInput.trigger(down);
            self.textInput.trigger(enter);
            equal(count, 1, "djselectableselect should only fire once.");
            start();
        }, 500);
    });
});