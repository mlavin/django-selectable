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
            if (type === 'combobox' || type === 'text') {
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
            } else if (type === 'hidden') {
                var hiddenName = $(input).attr('name');
                var textName = hiddenName.replace('_1', '_0');
                $(":input[name=" + textName + "][data-selectable-url]").bind("autocompletechange", function(event, ui) {
                    if (ui.item && ui.item.id) {
                        $(input).val(ui.item.id);
                    } else {
                        $(input).val("");
                    }
                });
            }
        }
	});

})(jQuery);

$(document).ready(function() {
    $(":input[data-selectable-type]").each(function(i, elem) {
        $(elem).djselectable();
    });
});
