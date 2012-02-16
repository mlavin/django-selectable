(function($) {

	$.widget("ui.djselectable", {

        options: {
            removeIcon: "ui-icon-close",
            comboboxIcon: "ui-icon-triangle-1-s",
            prepareQuery: null,
            highlightMatch: true,
            formatLabel: null
        },
        
        _initDeck: function(hiddenInputs) {
            var self = this;
            var data = $(this.element).data();
            var style = data.selectablePosition || data['selectable-position'] || 'bottom';
            this.deck = $('<ul>').addClass('ui-widget selectable-deck selectable-deck-' + style);
            if (style === 'bottom' || style === 'bottom-inline') {
                $(this.element).after(this.deck);
            } else {
                $(this.element).before(this.deck);
            }
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
                    $('<a>')
                    .attr('href', '#')
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
            var allowNew = data.selectableAllowNew || data['selectable-allow-new'];
            var allowMultiple = data.selectableMultiple || data['selectable-multiple'];
            var textName = $(input).attr('name');
            var hiddenName = textName.replace('_0', '_1');
            var hiddenSelector = 'input[type=hidden][data-selectable-type=hidden-multiple][name=' + hiddenName + ']';
            if (allowMultiple) {
                allowNew = false;
                $(input).val("");
                this._initDeck(hiddenSelector);
            }

            function dataSource(request, response) {
                var url = data.selectableUrl || data['selectable-url'];
                var now = new Date().getTime();
                var query = {term: request.term, timestamp: now};
                if (self.options.prepareQuery) {
                    self.options.prepareQuery(query);
                }
                var page = $(input).data("page");
                if (page) {
                    query.page = page;
                }
				$.getJSON(url, query, response);
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
                    if (ui.item && ui.item.page) {
                        $(input).data("page", ui.item.page);
                        $('.selectable-paginator', self.menu).remove();
                        $(input).autocomplete("search");
                        return false;
                    }
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
            $(input).data("autocomplete")._renderItem = function(ul, item) {
                var label = item.label;
                if (self.options.formatLabel) {
                    label = self.options.formatLabel(label, item);
                }
                if (self.options.highlightMatch) {
                    var re = new RegExp("(?![^&;]+;)(?!<[^<>]*)(" +
                    $.ui.autocomplete.escapeRegex(this.term) +
                    ")(?![^<>]*>)(?![^&;]+;)", "gi");
                    label = label.replace(re, "<span class='highlight'>$1</span>");
                }
                var li =  $("<li></li>")
			        .data("item.autocomplete", item)
			        .append($("<a></a>").append(label))
			        .appendTo(ul);
                if (item.page) {
                    li.addClass('selectable-paginator');
                }
	            return li;
            };
            $(input).data("autocomplete")._suggest = function(items) {
                var page = $(input).data('page');
                var ul = this.menu.element;
                if (!page) {
                    ul.empty();
                }
                $(input).data('page', null);
			    ul.zIndex(this.element.zIndex() + 1);
		        this._renderMenu(ul, items);
	            this.menu.deactivate();
                this.menu.refresh();
		        // size and position menu
		        ul.show();
		        this._resizeMenu();
		        ul.position($.extend({of: this.element}, this.options.position));
		        if (this.options.autoFocus) {
			        this.menu.next(new $.Event("mouseover"));
		        }
	        };
            var selectableType = data.selectableType || data['selectable-type'];
            if (selectableType === 'combobox') {
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
        $(":input[name=" + textName + "][data-selectable-url]").bind(
            "autocompletechange autocompleteselect",
            function(event, ui) {
                if (ui.item && ui.item.id) {
                    $(elem).val(ui.item.id);
                } else {
                    $(elem).val("");
                }
            }
        );
    });
}

if (typeof(django) != "undefined" && typeof(django.jQuery) != "undefined") {
    if (django.jQuery.fn.formset) {
        var oldformset = django.jQuery.fn.formset;
	    django.jQuery.fn.formset = function(opts) {
            var options = $.extend({}, opts);
            var addedevent = function(row) {
                bindSelectables($(row));
            };
            var added = null;
            if (options.added) {
                var oldadded = options.added;
                added = function(row) { oldadded(row); addedevent(row); };
            }
            options.added = added || addedevent;
            return oldformset.call(this, options);
        };
    }
}

$(document).ready(function() {
    bindSelectables('body');
});
