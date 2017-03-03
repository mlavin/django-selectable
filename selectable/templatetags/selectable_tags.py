from __future__ import unicode_literals

from django import template
from django.conf import settings
from selectable.registry import ChainedFormRegistry
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('selectable/jquery-js.html')
def include_jquery_libs(version='1.11.2', ui='1.11.3'):
    return {'version': version, 'ui': ui}


@register.inclusion_tag('selectable/jquery-css.html')
def include_ui_theme(theme='smoothness', version='1.11.3'):
    return {'theme': theme, 'version': version}


@register.filter
def bind_chained_form(form):
    """
    Generate JavaScript in order to send new parameters to a lookup
    """
    field_1, field_2 = ChainedFormRegistry.get(form)
    if field_1 is None:
        return ""

    for field in form:
        if field.name == field_1:
            child = field.id_for_label

        if field.name == field_2:
            if field.id_for_label.endswith('_0'):
                parent = field.id_for_label[:-1] + '1'
            else :
                parent = field.id_for_label

    return mark_safe("$(document).ready(function() {{\n" \
                     "   function newParameters(query) {{\n" \
                     "       query.state = $('#{parent}').val();\n" \
                     "    }}\n" \
                     "    $('#{child}').djselectable('option', 'prepareQuery', newParameters);\n" \
                     "}});".format(parent=parent, child=child))

