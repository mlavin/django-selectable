from django.test.client import Client
from django.utils import simplejson as json

from selectable.tests import ThingLookup
from selectable.tests.base import BaseSelectableTestCase


__all__ = (
    'SelectableViewTest',
)


class SelectableViewTest(BaseSelectableTestCase):
    
    def setUp(self):
        super(SelectableViewTest, self).setUp()
        self.client = Client()
        self.url = ThingLookup.url()
        self.lookup = ThingLookup()
        self.thing = self.create_thing()
        self.other_thing = self.create_thing()

    def test_response_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_response_keys(self):
        response = self.client.get(self.url)
        data = json.loads(response.content)
        for result in data:
            self.assertTrue('id' in result)
            self.assertTrue('value' in result)
            self.assertTrue('label' in result)

    def test_no_term_lookup(self):
        data = {}
        response = self.client.get(self.url, data)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_simple_term_lookup(self):
        data = {'term': self.thing.name}
        response = self.client.get(self.url, data)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
            
