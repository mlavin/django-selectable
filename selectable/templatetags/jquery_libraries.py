# -*- encoding: utf-8 -*-
from django import template
from django.template import Library
from django.conf import settings

register = template.Library()

@register.simple_tag
def include_jquery_libs():
    SCRIPT_TAG = '<script type="text/javascript" src="%s"></script>'

    try:
        jquery_url = settings.JQUERY_URL
    except:
        jquery_url = '//ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js'

    try:
        jquery_ui_url = settings.JQUERY_UI_URL
    except:
        jquery_ui_url = '//ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js'

    script_libs = SCRIPT_TAG % jquery_url
    script_libs += '\n'
    script_libs += SCRIPT_TAG % jquery_ui_url
    return script_libs


