(function($) {
	$.widget("ui.djselectable", {
        _create: function() {
            var self = $(this),
            input = this.element;
            type = $(input).attr('data-selectable-type');
            url = $(input).attr('data-selectable-url');
            
            var allowAttr = $(input).attr('data-selectable-allow-new');
            var allowNew = false;
            if (typeof allowAttr !== 'undefined' && allowAttr === 'true') {
                allowNew = true;
            }

            var multipleAttr = $(input).attr('data-selectable-multiple');
            var allowMultiple = false;
            var deck = null;
            var textName = $(input).attr('name');
            var hiddenName = textName.replace('_0', '_1');
            var hiddenSelector = 'input[type=hidden][data-selectable-type=hidden-multiple][name=' + hiddenName + ']';
            if (typeof multipleAttr !== 'undefined' && multipleAttr === 'true') {
                allowMultiple = true;
                allowNew = false;
                $(input).val("");
                deck = $('<ul>').addClass('ui-widget selectable-deck');
                $(input).after(deck);
                $(hiddenSelector).each(function(i, elem) {
                    $('<li>')
                    .text($(elem).attr('title'))
                    .addClass('selectable-deck-item')
                    .appendTo(deck)
                    .append(
                        $('<div>')
                        .addClass('selectable-deck-remove')
                        .append(
                            $('<button>')
                            .button({
                                icons: {
                                    primary: "ui-icon-close"
                                },
                                text: false
                            })
                            .click(function() {
                                $(elem).remove();
                                $(this).parents('li').remove();
                            })
                        )
                    );
                });
            }

            $(input).autocomplete({
                source: url,
                change: function(event, ui) {
                    if (!ui.item) {
                        if (!allowNew) {
                            $(input).val("");
			                $(input).data("autocomplete").term = "";
			                return false;
                        } 
                    } 
                    if (allowMultiple) {
                        $(input).val("");
	                    $(input).data("autocomplete").term = "";
                    }
                },
                select: function(event, ui) {
                    if (ui.item && allowMultiple) {
                        $(input).val("");
		                $(input).data("autocomplete").term = "";
                        if ($(hiddenSelector + '[value=' + ui.item.id + ']').length === 0) {
                            // TODO: This won't work in IE...
                            var newInput = $('<input>').attr({
                                type: 'hidden',
                                name: hiddenName,
                                value: ui.item.id,
                                title: ui.item.value
                            });
                            $(input).after(newInput);
                            $('<li>')
                            .text(ui.item.value)
                            .addClass('selectable-deck-item')
                            .appendTo(deck)
                            .append(
                                $('<div>')
                                .addClass('selectable-deck-remove')
                                .append(
                                    $('<button>')
                                    .button({
                                        icons: {
                                            primary: "ui-icon-close"
                                        },
                                        text: false
                                    })
                                    .click(function() {
                                        newInput.remove();
                                        $(this).parents('li').remove();
                                    })
                                )
                            );
                        }
                    }
                }
            }).addClass("ui-widget ui-widget-content ui-corner-all");
            if (type === 'combobox') {
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
                        primary: "ui-icon-triangle-1-s"
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

$(document).ready(function() {
    $(":input[data-selectable-type=text]").djselectable();
    $(":input[data-selectable-type=combobox]").djselectable();
    $(":input[data-selectable-type=hidden]").each(function(i, elem) {
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
});
