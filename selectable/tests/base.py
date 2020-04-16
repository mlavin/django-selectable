import random
import string
from collections import defaultdict


from django.test import TestCase, override_settings
from django.test.html import parse_html

from . import Thing
from ..base import ModelLookup


def parsed_inputs(html):
    "Returns a dictionary mapping name --> node of inputs found in the HTML."
    node = parse_html(html)
    inputs = {}
    for field in [c for c in node.children if c.name == 'input']:
        name = dict(field.attributes)['name']
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


def parsed_widget_attributes(widget):
    """
    Get a dictionary-like object containing all HTML attributes
    of the rendered widget.

    Lookups on this object raise ValueError if there is more than one attribute
    of the given name in the HTML, and they have different values.
    """
    # For the tests that use this, it generally doesn't matter what the value
    # is, so we supply anything.
    rendered = widget.render('a_name', 'a_value')
    return AttrMap(rendered)


class AttrMap():
    def __init__(self, html):
        dom = parse_html(html)
        self._attrs = defaultdict(set)
        self._build_attr_map(dom)

    def _build_attr_map(self, dom):
        for node in _walk_nodes(dom):
            if node.attributes is not None:
                for (k, v) in node.attributes:
                    self._attrs[k].add(v)

    def __contains__(self, key):
        return key in self._attrs and len(self._attrs[key]) > 0

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)
        vals = self._attrs[key]
        if len(vals) > 1:
            raise ValueError("More than one value for attribute {0}: {1}".
                             format(key, ", ".join(vals)))
        else:
            return list(vals)[0]


def _walk_nodes(dom):
    yield dom
    for child in dom.children:
        for item in _walk_nodes(child):
            yield item
