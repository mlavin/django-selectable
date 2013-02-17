/*jshint trailing:true, indent:4*/
/*
 * django-selectable UI widget
 * Source: https://bitbucket.org/mlavin/django-selectable
 * Docs: http://django-selectable.readthedocs.org/
 *
 * Depends:
 *   - jQuery 1.4.4+
 *   - jQuery UI 1.8 widget factory
 *
 * Copyright 2010-2013, Mark Lavin
 * BSD License
 *
*/
(function ($) {

	$.widget("ui.djselectable", $.ui.autocomplete, {

        options: {
            removeIcon: "ui-icon-close",
            comboboxIcon: "ui-icon-triangle-1-s",
            defaultClasses: {
                "text": "ui-widget ui-widget-content ui-corner-all",
                "combobox": "ui-widget ui-widget-content ui-corner-left ui-combo-input"
            },
            prepareQuery: null,
            highlightMatch: true,
            formatLabel: null
        },

        _initDeck: function () {
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
            $(self.hiddenMultipleSelector).each(function (i, input) {
                self._addDeckItem(input);
            });
        },

        _addDeckItem: function (input) {
            /* Add new deck list item from a given hidden input */
            var self = this,
                li = $('<li>').addClass('selectable-deck-item'),
                item = {element: self.element, input: input, wrapper: li, deck: self.deck},
                button;
            li.html($(input).attr('title'));
            if (self._trigger("add", null, item) === false) {
                input.remove();
            } else {
                button = this._removeButtonTemplate(item);
                button.click(function (e) {
                    e.preventDefault();
                    if (self._trigger("remove", e, item) !== false) {
                        $(input).remove();
                        li.remove();
                    }
                });
                li.append(button).appendTo(this.deck);
            }
        },

        _removeButtonTemplate: function (item) {
            var options = {
                    icons: {
                        primary: this.options.removeIcon
                    },
                    text: false
                },
                button = $('<a>')
                .attr('href', '#')
                .addClass('selectable-deck-remove')
                .button(options);
            return button;
        },

        select: function (item, event) {
            /* Trigger selection of a given item.
            Item should contain two properties: id and value
            Event is the original select event if there is one.
            Event should not be passed if triggered manually.
            */
            var $input = $(this.element);
            $input.removeClass('ui-state-error');
            this._setHidden(item);
            if (item) {
                if (this.allowMultiple) {
                    $input.val("");
                    this.term = "";
                    if ($(this.hiddenMultipleSelector + '[value="' + item.id + '"]').length === 0) {
                        var newInput = $('<input />', {
                            'type': 'hidden',
                            'name': this.hiddenName,
                            'value': item.id,
                            'title': item.value,
                            'data-selectable-type': 'hidden-multiple'
                        });
                        $input.after(newInput);
                        this._addDeckItem(newInput);
                    }
                    return false;
                } else {
                    $input.val(item.value);
                    var ui = {item: item};
                    if (typeof(event) === 'undefined' || event.type !== "djselectableselect") {
                        this.element.trigger("djselectableselect", [ui ]);
                    }
                }
            }
        },

        _setHidden: function (item) {
            /* Set or clear single hidden input */
            var $elem = $(this.hiddenSelector);
            if (item && item.id) {
                $elem.val(item.id);
            } else {
                $elem.val("");
            }
        },

        _comboButtonTemplate: function (input) {
            // Add show all items button
            var options = {
                    icons: {
                        primary: this.options.comboboxIcon
                    },
                    text: false
                },
                button = $("<a>")
                    .html("&nbsp;")
                    .attr("tabIndex", -1)
                    .attr("title", "Show All Items")
                    .button(options)
                    .removeClass("ui-corner-all")
                    .addClass("ui-corner-right ui-button-icon ui-combo-button");
            return button;
        },

        _create: function () {
            /* Initialize a new selectable widget */
            var self = this,
            $input = $(this.element),
            data = $input.data(),
            options, button;
            this.url = data.selectableUrl || data['selectable-url'];
            this.allowNew = data.selectableAllowNew || data['selectable-allow-new'];
            this.allowMultiple = data.selectableMultiple || data['selectable-multiple'];
            this.textName = $input.attr('name');
            this.hiddenName = this.textName.replace(new RegExp('_0$'), '_1');
            this.hiddenSelector = ':input[data-selectable-type=hidden][name=' + this.hiddenName + ']';
            this.hiddenMultipleSelector = ':input[data-selectable-type=hidden-multiple][name=' + this.hiddenName + ']';
            this.selectableType = data.selectableType || data['selectable-type'];
            if (this.allowMultiple) {
                this.allowNew = false;
                $input.val("");
                this._initDeck();
            }
            options = data.selectableOptions || data['selectable-options'];
            if (options) {
                this._setOptions(options);
            }
            // Call super-create
            // This could be replaced by this._super() with jQuery UI 1.9
            $.ui.autocomplete.prototype._create.call(this);
            $input.addClass(this.options.defaultClasses[this.selectableType]);
            // Additional work for combobox widgets
            if (this.selectableType === 'combobox') {
                // Add show all items button
                button = this._comboButtonTemplate($input);
                button.insertAfter($input).click(function (e) {
                    e.preventDefault();
                    // close if already visible
                    if (self.widget().is(":visible")) {
                        self.close();
                    }
                    // pass empty string as value to search for, displaying all results
                    self._search("");
                    $input.focus();
                });
            }
        },

        // Override the default source creation
        _initSource: function () {
            var self = this,
                $input = $(this.element);
            this.source = function dataSource(request, response) {
                /* Custom data source to uses the lookup url with pagination
                Adds hook for adjusting query parameters.
                Includes timestamp to prevent browser caching the lookup. */
                var now = new Date().getTime(),
                    query = {term: request.term, timestamp: now},
                    page = $input.data("page");
                if (self.options.prepareQuery) {
                    self.options.prepareQuery.apply(self, [query]);
                }
                if (page) {
                    query.page = page;
                }
                function unwrapResponse(data) {
                    var results = data.data,
                        meta = data.meta;
                    if (meta.next_page && meta.more) {
                        results.push({
                            id: '',
                            value: '',
                            label: meta.more,
                            page: meta.next_page,
                            term: request.term
                        });
                    }
                    return response(results);
                }
				$.getJSON(self.url, query, unwrapResponse);
            };
        },
        // Override the default auto-complete render.
        _renderItem: function (ul, item) {
            /* Adds hook for additional formatting, allows HTML in the label,
            highlights term matches and handles pagination. */
            var label = item.label,
                self = this,
                $input = $(this.element),
                re, html, li;
            if (this.options.formatLabel && !item.page) {
                label = this.options.formatLabel.apply(this, [label, item]);
            }
            if (this.options.highlightMatch && this.term && !item.page) {
                re = new RegExp("(?![^&;]+;)(?!<[^<>]*)(" +
                    $.ui.autocomplete.escapeRegex(this.term) +
                    ")(?![^<>]*>)(?![^&;]+;)", "gi");
                if (label.html) {
                    html = label.html();
                    html = html.replace(re, "<span class='highlight'>$1</span>");
                    label.html(html);
                } else {
                    label = label.replace(re, "<span class='highlight'>$1</span>");
                }
            }
            li = $("<li></li>")
                .data("item.autocomplete", item)
                .append($("<a></a>").append(label))
                .appendTo(ul);
            if (item.page) {
                li.addClass('selectable-paginator');
            }
            return li;
        },
        // Override the default auto-complete suggest.
        _suggest: function (items) {
            /* Needed for handling pagination links */
            var $input = $(this.element),
                page = $input.data('page'),
                ul = this.menu.element;
            if (page) {
                $('.selectable-paginator', ul).remove();
            } else {
                ul.empty();
            }
            $input.data('page', null);
            ul.zIndex($input.zIndex() + 1);
            this._renderMenu(ul, items);
            // jQuery UI menu does not define deactivate
            if (this.menu.deactivate) {
                this.menu.deactivate();
            }
            this.menu.refresh();
            // size and position menu
            ul.show();
            this._resizeMenu();
            ul.position($.extend({of: this.element}, this.options.position));
            if (this.options.autoFocus) {
                this.menu.next(new $.Event("mouseover"));
            } else if (page) {
                $input.focus();
            }
        },
        // Override default trigger for additional change/select logic
        _trigger: function (type, event, data) {
            var $input = $(this.element),
                self = this;
            if (type === "select") {
                $input.removeClass('ui-state-error');
                if (data.item.page) {
                    $input.data("page", data.item.page);
                    this._search(data.item.term);
                    return false;
                }
                return this.select(data.item, event);
            } else if (type === "change") {
                $input.removeClass('ui-state-error');
                this._setHidden(data.item);
                if ($input.val() && !data.item) {
                    if (!this.allowNew) {
                        $input.addClass('ui-state-error');
                    }
                }
                if (this.allowMultiple && !$input.hasClass('ui-state-error')) {
                    $input.val("");
                    this.term = "";
                }
            }
            // Call super trigger
            // This could be replaced by this._super() with jQuery UI 1.9
            return $.ui.autocomplete.prototype._trigger.apply(this, arguments);
        },
        close: function (event) {
            var page = $(this.element).data('page');
            if (page != null) {
                return;
            }
            // Call super trigger
            // This could be replaced by this._super() with jQuery UI 1.9
            return $.ui.autocomplete.prototype.close.apply(this, arguments);
        }
	});

    window.bindSelectables = function (context) {
        /* Bind all selectable widgets in a given context.
        Automatically called on document.ready.
        Additional calls can be made for dynamically added widgets.
        */
        $(":input[data-selectable-type=text]", context).djselectable();
        $(":input[data-selectable-type=combobox]", context).djselectable();
    };

    function djangoAdminPatches() {
        /* Monkey-patch Django's dynamic formset, if defined */
        if (typeof(django) !== "undefined" && typeof(django.jQuery) !== "undefined") {
            if (django.jQuery.fn.formset) {
                var oldformset = django.jQuery.fn.formset;
                django.jQuery.fn.formset = function (opts) {
                    var options = $.extend({}, opts);
                    var addedevent = function (row) {
                        window.bindSelectables($(row));
                    };
                    var added = null;
                    if (options.added) {
                        // Wrap previous added function and include call to bindSelectables
                        var oldadded = options.added;
                        added = function (row) { oldadded(row); addedevent(row); };
                    }
                    options.added = added || addedevent;
                    return oldformset.call(this, options);
                };
            }
        }

        /* Monkey-patch Django's dismissAddAnotherPopup(), if defined */
        if (typeof(dismissAddAnotherPopup) !== "undefined" &&
            typeof(windowname_to_id) !== "undefined" &&
            typeof(html_unescape) !== "undefined") {
            var django_dismissAddAnotherPopup = dismissAddAnotherPopup;
            dismissAddAnotherPopup = function (win, newId, newRepr) {
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
    }

    $(document).ready(function () {
        // Patch the django admin JS
        if (typeof(djselectableAdminPatch) === "undefined" || djselectableAdminPatch) {
            djangoAdminPatches();
        }
        // Bind existing widgets on document ready
        if (typeof(djselectableAutoLoad) === "undefined" || djselectableAutoLoad) {
            window.bindSelectables('body');
        }
    });
})(jQuery || grp.jQuery);
