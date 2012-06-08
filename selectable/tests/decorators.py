from mock import Mock

from selectable.decorators import ajax_required, login_required, staff_member_required
from selectable.tests.base import BaseSelectableTestCase, SimpleModelLookup


__all__ = (
    'AjaxRequiredLookupTestCase',
    'LoginRequiredLookupTestCase',
    'StaffRequiredLookupTestCase',
)


class AjaxRequiredLookupTestCase(BaseSelectableTestCase):

    def setUp(self):
        self.lookup = ajax_required(SimpleModelLookup)()

    def test_ajax_call(self):
        "Ajax call should yield a successful response."
        request = Mock()
        request.is_ajax = lambda: True
        response = self.lookup.results(request)
        self.assertTrue(response.status_code, 200)

    def test_non_ajax_call(self):
        "Non-Ajax call should yield a bad request response."
        request = Mock()
        request.is_ajax = lambda: False
        response = self.lookup.results(request)
        self.assertEqual(response.status_code, 400)


class LoginRequiredLookupTestCase(BaseSelectableTestCase):

    def setUp(self):
        self.lookup = login_required(SimpleModelLookup)()
    
    def test_authenicated_call(self):
        "Authenicated call should yield a successful response."
        request = Mock()
        user = Mock()
        user.is_authenticated = lambda: True
        request.user = user
        response = self.lookup.results(request)
        self.assertTrue(response.status_code, 200)

    def test_non_authenicated_call(self):
        "Non-Authenicated call should yield an unauthorized response."
        request = Mock()
        user = Mock()
        user.is_authenticated = lambda: False
        request.user = user
        response = self.lookup.results(request)
        self.assertEqual(response.status_code, 401)


class StaffRequiredLookupTestCase(BaseSelectableTestCase):

    def setUp(self):
        self.lookup = staff_member_required(SimpleModelLookup)()

    def test_staff_member_call(self):
        "Staff member call should yield a successful response."
        request = Mock()
        user = Mock()
        user.is_authenticated = lambda: True
        user.is_staff = True
        request.user = user
        response = self.lookup.results(request)
        self.assertTrue(response.status_code, 200)

    def test_authenicated_but_not_staff(self):
        "Authenicated but non staff call should yield a forbidden response."
        request = Mock()
        user = Mock()
        user.is_authenticated = lambda: True
        user.is_staff = False
        request.user = user
        response = self.lookup.results(request)
        self.assertTrue(response.status_code, 403)

    def test_non_authenicated_call(self):
        "Non-Authenicated call should yield an unauthorized response."
        request = Mock()
        user = Mock()
        user.is_authenticated = lambda: False
        user.is_staff = False
        request.user = user
        response = self.lookup.results(request)
        self.assertEqual(response.status_code, 401)
