from django import template

register = template.Library()


@register.inclusion_tag('selectable/jquery-js.html')
def include_jquery_libs(version='1.12.4', ui='1.11.4'):
    return {'version': version, 'ui': ui}


@register.inclusion_tag('selectable/jquery-css.html')
def include_ui_theme(theme='smoothness', version='1.11.4'):
    return {'theme': theme, 'version': version}
