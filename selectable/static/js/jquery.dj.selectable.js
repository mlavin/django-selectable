$(document).ready(function() {
    $(":input[data-selectable-url]").each(function(i, elem) {
        var url = $(elem).attr('data-selectable-url');
        $(elem).autocomplete({
            source: url,
            change: function(event, ui) {
                var allowAttr = $(this).attr('data-selectable-allow-new');
                var allowNew = false;
                if (typeof allowAttr !== 'undefined' && allowAttr === 'true') {
                    allowNew = true;
                }
                if (!ui.item) {
                    if (!allowNew) {
                        $(this).val("");
					    $(this).data("autocomplete").term = "";
					    return false;
                    }
                }
            }
        });
        if ($(elem).attr('data-selectable-type') === 'combobox') {
            // Change auto-complete options
            $(elem).autocomplete("option", {
                delay: 0,
                minLength: 0
            });

            $("<button>&nbsp;</button>").attr("tabIndex", -1).attr("title", "Show All Items")
            .insertAfter($(elem))
            .button({
                icons: {
                    primary: "ui-icon-triangle-1-s"
                },
                text: false
            })
            .click(function() {
                console.log('Click!');
                // close if already visible
                if ($(elem).autocomplete("widget").is(":visible")) {
                    $(elem).autocomplete("close");
                    return false;
                }

                // pass empty string as value to search for, displaying all results
                $(elem).autocomplete("search", "");
                $(elem).focus();
                return false;
            });
        }
    });
    $(":input[data-selectable-is-hidden]").each(function(i, elem) {
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
