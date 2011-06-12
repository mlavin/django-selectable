from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.utils import simplejson as json

from selectable.tests import ThingLookup
from selectable.tests.base import BaseSelectableTestCase, PatchSettingsMixin


__all__ = (
    'SelectableViewTest',
)


def test_404(request):
    return HttpResponseNotFound()


def test_500(request):
    return HttpResponseServerError()


class SelectableViewTest(PatchSettingsMixin, BaseSelectableTestCase):
    
    def setUp(self):
        super(SelectableViewTest, self).setUp()
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

    def test_unknown_lookup(self):
        unknown_url = reverse('selectable-lookup', args=["XXXXXXX"])
        response = self.client.get(unknown_url)
        self.assertEqual(response.status_code, 404)

    def test_basic_limit(self):
        for i in range(settings.SELECTABLE_MAX_LIMIT):
            self.create_thing(data={'name': 'Thing%s' % i})
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertEqual(len(data), settings.SELECTABLE_MAX_LIMIT + 1)
        last_item = data[-1]
        self.assertTrue('page' in last_item)

    def test_get_next_page(self):
        for i in range(settings.SELECTABLE_MAX_LIMIT * 2):
            self.create_thing(data={'name': 'Thing%s' % i})
        data = {'term': 'Thing', 'page': 2}
        response = self.client.get(self.url, data)
        data = json.loads(response.content)
        self.assertEqual(len(data), settings.SELECTABLE_MAX_LIMIT)
        # No next page
        last_item = data[-1]
        self.assertFalse('page' in last_item)

    def test_request_more_than_max(self):
        for i in range(settings.SELECTABLE_MAX_LIMIT):
            self.create_thing(data={'name': 'Thing%s' % i})
        data = {'term': '', 'limit': settings.SELECTABLE_MAX_LIMIT * 2}
        response = self.client.get(self.url)
        data = json.loads(response.content)
        self.assertEqual(len(data), settings.SELECTABLE_MAX_LIMIT + 1)

    def test_request_less_than_max(self):
        for i in range(settings.SELECTABLE_MAX_LIMIT):
            self.create_thing(data={'name': 'Thing%s' % i})
        new_limit = settings.SELECTABLE_MAX_LIMIT / 2
        data = {'term': '', 'limit': new_limit}
        response = self.client.get(self.url, data)
        data = json.loads(response.content)
        self.assertEqual(len(data), new_limit + 1)

