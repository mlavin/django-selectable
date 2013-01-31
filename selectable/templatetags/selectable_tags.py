from __future__ import unicode_literals

from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag('selectable/jquery-js.html')
def include_jquery_libs(version='1.7.2', ui='1.8.23'):
    return {'version': version, 'ui': ui}


@register.inclusion_tag('selectable/jquery-css.html')
def include_ui_theme(theme='base', version='1.8.23'):
    return {'theme': theme, 'version': version}
