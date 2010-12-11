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
});
