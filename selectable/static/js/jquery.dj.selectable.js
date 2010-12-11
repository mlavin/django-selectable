$(document).ready(function() {
    $(":input[data-selectable-url]").each(function(i, elem) {
        var url = $(elem).attr('data-selectable-url');
        $(elem).autocomplete({source: url});
    });
});
