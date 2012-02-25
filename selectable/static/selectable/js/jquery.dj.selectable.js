/* 
 * django-selectable UI widget
 * Source: https://bitbucket.org/mlavin/django-selectable
 * Docs: http://django-selectable.readthedocs.org/
 *
 * Depends:
 *   - jQuery 1.4.3+
 *   - jQuery UI 1.8 widget factory
 *
 * Copyright 2010-2012, Mark Lavin
 * BSD License
 *
*/
(function($) {

	$.widget("ui.djselectable", {

        options: {
            removeIcon: "ui-icon-close",
            comboboxIcon: "ui-icon-triangle-1-s",
            prepareQuery: null,
            highlightMatch: true,
            formatLabel: null
        },
        
        _initDeck: function() {
            /* Create list display for currently selected items for multi-select */
            var self = this;
            var data = $(this.element).data();
            var style = data.selectablePosition || data['selectable-position'] || 'bottom';
            this.deck = $('<ul>').addClass('ui-widget selectable-deck selectable-deck-' + style);
            if (style === 'bottom' || style === 'bottom-inline') {
                $(this.element).after(this.deck);
            } else {
                $(this.element).before(this.deck);
            }
            $(self.hiddenMultipleSelector).each(function(i, input) {
                self._addDeckItem(input);
            });
        },

        _addDeckItem: function(input) {
            /* Add new deck list item from a given hidden input */
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

        select: function(item) {
            /* Trigger selection of a given item.
            Item should contain two properties: id and value */
            var self = this,
            input = this.element;
            $(input).removeClass('ui-state-error');
            if (item) {
                if (self.allowMultiple) {
                    $(input).val("");
                    $(input).data("autocomplete").term = "";
                    if ($(self.hiddenMultipleSelector + '[value=' + item.id + ']').length === 0) {
                        var newInput = $('<input />', {
                            'type': 'hidden',
                            'name': self.hiddenName,
                            'value': item.id,
                            'title': item.value,
                            'data-selectable-type': 'hidden-multiple'
                        });
                        $(input).after(newInput);
                        self._addDeckItem(newInput);
                        return false;
                    }
                } else {
                    $(input).val(item.value);
                    var ui = {item: item};
                    $(input).trigger('autocompleteselect', [ui ]);
                }
            }
        },

        _create: function() {
            /* Initialize a new selectable widget */
            var self = this,
            input = this.element,
            data = $(input).data();
            self.allowNew = data.selectableAllowNew || data['selectable-allow-new'];
            self.allowMultiple = data.selectableMultiple || data['selectable-multiple'];
            self.textName = $(input).attr('name');
            self.hiddenName = self.textName.replace('_0', '_1');
            self.hiddenSelector = ':input[data-selectable-type=hidden][name=' + self.hiddenName + ']';
            self.hiddenMultipleSelector = ':input[data-selectable-type=hidden-multiple][name=' + self.hiddenName + ']';
            if (self.allowMultiple) {
                self.allowNew = false;
                $(input).val("");
                this._initDeck();
            }

            function dataSource(request, response) {
                /* Custom data source to uses the lookup url with pagination
                Adds hook for adjusting query parameters.
                Includes timestamp to prevent browser caching the lookup. */
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
            // Create base auto-complete lookup
            $(input).autocomplete({
                source: dataSource,
                change: function(event, ui) {
                    $(input).removeClass('ui-state-error');
                    if ($(input).val() && !ui.item) {
                        if (!self.allowNew) {
                            $(input).addClass('ui-state-error');
                        } 
                    } 
                    if (self.allowMultiple && !$(input).hasClass('ui-state-error')) {
                        $(input).val("");
                        $(input).data("autocomplete").term = "";
                    }
                },
                select: function(event, ui) {
                    $(input).removeClass('ui-state-error');
                    if (ui.item && ui.item.page) {
                        // Set current page value
                        $(input).data("page", ui.tem.page);
                        $('.selectable-paginator', self.menu).remove();
                        // Search for next page of results
                        $(input).autocomplete("search");
                        return false;
                    }
                    self.select(ui.item);
                }
            }).addClass("ui-widget ui-widget-content ui-corner-all");
            // Override the default auto-complete render.
            $(input).data("autocomplete")._renderItem = function(ul, item) {
                /* Adds hook for additional formatting, allows HTML in the label,
                highlights term matches and handles pagination. */
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
            // Override the default auto-complete suggest.
            $(input).data("autocomplete")._suggest = function(items) {
                /* Needed for handling pagination links */
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
            // Additional work for combobox widgets
            var selectableType = data.selectableType || data['selectable-type'];
            if (selectableType === 'combobox') {
                // Change auto-complete options
                $(input).autocomplete("option", {
                    delay: 0,
                    minLength: 0
                })
                .removeClass("ui-corner-all")
                .addClass("ui-corner-left ui-combo-input");
                // Add show all items button
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
    /* Bind all selectable widgets in a given context.
    Automatically called on document.ready.
    Additional calls can be made for dynamically added widgets.
    */
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

/* Monkey-patch Django's dynamic formset, if defined */
if (typeof(django) !== "undefined" && typeof(django.jQuery) !== "undefined") {
    if (django.jQuery.fn.formset) {
        var oldformset = django.jQuery.fn.formset;
        django.jQuery.fn.formset = function(opts) {
            var options = $.extend({}, opts);
            var addedevent = function(row) {
                bindSelectables($(row));
            };
            var added = null;
            if (options.added) {
                // Wrap previous added function and include call to bindSelectables
                var oldadded = options.added;
                added = function(row) { oldadded(row); addedevent(row); };
            }
            options.added = added || addedevent;
            return oldformset.call(this, options);
        };
    }
}

/* Monkey-patch Django's dismissAddAnotherPopup(), if defined */
if (typeof(dismissAddAnotherPopup) !== "undefined" && typeof(windowname_to_id) !== "undefined" && typeof(html_unescape) !== "undefined") {
    var django_dismissAddAnotherPopup = dismissAddAnotherPopup;
    dismissAddAnotherPopup = function(win, newId, newRepr) {
        /* See if the popup came from a selectable field.
           If not, pass control to Django's code.
           If so, handle it. */
        var fieldName = windowname_to_id(win.name); /* e.g. "id_fieldname" */
        var field = $('#' + fieldName);
        var multiField = $('#' + fieldName + '_0');
        /* Check for bound selectable */
        var singleWidget = field.data('djselectable');
        var multiWidget = multiField.data('djselectable');
        if (singleWidget || multiWidget) {
            // newId and newRepr are expected to have previously been escaped by
            // django.utils.html.escape.
            var item =  {
                id: html_unescape(newId),
                value: html_unescape(newRepr)
            };
            if (singleWidget) {
                field.djselectable('select', item);
            }
            if (multiWidget) {
                multiField.djselectable('select', item);
            }
            win.close();
        } else {
            /* Not ours, pass on to original function. */
            return django_dismissAddAnotherPopup(win, newId, newRepr);
        }
    };
}

$(document).ready(function() {
    // Bind existing widgets on document ready
    if (typeof(djselectableAutoLoad) === "undefined" || djselectableAutoLoad) {
        bindSelectables('body');
    }
});
