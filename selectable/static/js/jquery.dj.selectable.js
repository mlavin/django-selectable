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
