(function($) {
	$.widget("ui.djselectable", {

        options: {
            removeIcon: "ui-icon-close",
            comboboxIcon: "ui-icon-triangle-1-s"
        },
        
        _initDeck: function(hiddenInputs) {
            var self = this;
            this.deck = $('<ul>').addClass('ui-widget selectable-deck');
            $(this.element).after(this.deck);
            $(hiddenInputs).each(function(i, input) {
                self._addDeckItem(input);
            });
        },

        _addDeckItem: function(input) {
            var self = this;
            $('<li>')
            .text($(input).attr('title'))
            .addClass('selectable-deck-item')
            .appendTo(this.deck)
            .append(
                $('<div>')
                .addClass('selectable-deck-remove')
                .append(
                    $('<button>')
                    .button({
                        icons: {
                            primary: self.options.removeIcon
                        },
                        text: false
                    })
                    .click(function() {
                        $(input).remove();
                        $(this).closest('li').remove();
                        return false;
                    })
                )
            );
        },

        _create: function() {
            var self = this,
            input = this.element;
            var data = $(input).data();
            var allowNew = data['selectable-allow-new'];
            var allowMultiple = data['selectable-multiple'];
            var textName = $(input).attr('name');
            var hiddenName = textName.replace('_0', '_1');
            var hiddenSelector = 'input[type=hidden][data-selectable-type=hidden-multiple][name=' + hiddenName + ']';
            if (allowMultiple) {
                allowNew = false;
                $(input).val("");
                this._initDeck(hiddenSelector);
            }

            function dataSource(request, response) {
                var url = data['selectable-url'];
                var now = new Date().getTime();
				$.getJSON(url, {
					term: request.term,
                    timestamp: now
				}, response);
            }

            $(input).autocomplete({
                source: dataSource,
                change: function(event, ui) {
                    $(input).removeClass('ui-state-error');
                    if ($(input).val() && !ui.item) {
                        if (!allowNew) {
                            $(input).addClass('ui-state-error');
                        } 
                    } 
                    if (allowMultiple && !$(input).hasClass('ui-state-error')) {
                        $(input).val("");
	                    $(input).data("autocomplete").term = "";
                    }
                },
                select: function(event, ui) {
                    $(input).removeClass('ui-state-error');
                    if (ui.item && allowMultiple) {
                        $(input).val("");
		                $(input).data("autocomplete").term = "";
                        if ($(hiddenSelector + '[value=' + ui.item.id + ']').length === 0) {
                            var newInput = $('<input />', {
                                'type': 'hidden',
                                'name': hiddenName,
                                'value': ui.item.id,
                                'title': ui.item.value,
                                'data-selectable-type': 'hidden-multiple'
                            });
                            $(input).after(newInput);
                            self._addDeckItem(newInput);
                            return false;
                        }
                    }
                }
            }).addClass("ui-widget ui-widget-content ui-corner-all");
            if (data['selectable-type'] === 'combobox') {
                // Change auto-complete options
                $(input).autocomplete("option", {
                    delay: 0,
                    minLength: 0
                })
                .removeClass("ui-corner-all")
                .addClass("ui-corner-left ui-combo-input");

                $("<button>&nbsp;</button>").attr("tabIndex", -1).attr("title", "Show All Items")
                .insertAfter($(input))
                .button({
                    icons: {
                        primary: self.options.comboboxIcon
                    },
                    text: false
                })
                .removeClass("ui-corner-all")
		        .addClass("ui-corner-right ui-button-icon ui-combo-button")
                .click(function() {
                    // close if already visible
                    if ($(input).autocomplete("widget").is(":visible")) {
                        $(input).autocomplete("close");
                        return false;
                    }

                    // pass empty string as value to search for, displaying all results
                    $(input).autocomplete("search", "");
                    $(input).focus();
                    return false;
                });
            }
        }
	});
})(jQuery);

function bindSelectables(context) {
    $(":input[data-selectable-type=text]", context).djselectable();
    $(":input[data-selectable-type=combobox]", context).djselectable();
    $(":input[data-selectable-type=hidden]", context).each(function(i, elem) {
        var hiddenName = $(elem).attr('name');
        var textName = hiddenName.replace('_1', '_0');
        $(":input[name=" + textName + "][data-selectable-url]").bind("autocompletechange", function(event, ui) {
            if (ui.item && ui.item.id) {
                $(elem).val(ui.item.id);
            } else {
                $(elem).val("");
            }
        });
    });
}

$(document).ready(function() {
    bindSelectables('body');
});
