from __future__ import unicode_literals

import random
import string
from xml.dom.minidom import parseString

from django.test import TestCase, override_settings

from ..base import ModelLookup
from . import Thing


def as_xml(html):
    "Convert HTML portion to minidom node."
    return parseString('<root>%s</root>' % html)


def parsed_inputs(html):
    "Returns a dictionary mapping name --> node of inputs found in the HTML."
    node = as_xml(html)
    inputs = {}
    for field in node.getElementsByTagName('input'):
        name = dict(field.attributes.items())['name']
        current = inputs.get(name, [])
        current.append(field)
        inputs[name] = current
    return inputs


@override_settings(ROOT_URLCONF='selectable.tests.urls')
class BaseSelectableTestCase(TestCase):

    def get_random_string(self, length=10):
        return ''.join(random.choice(string.ascii_letters) for x in range(length))

    def create_thing(self, data=None):
        data = data or {}
        defaults = {
            'name': self.get_random_string(),
            'description': self.get_random_string(),
        }
        defaults.update(data)
        return Thing.objects.create(**defaults)


class SimpleModelLookup(ModelLookup):
    model = Thing
    search_fields = ('name__icontains', )
