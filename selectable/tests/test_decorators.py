from unittest.mock import Mock

from ..decorators import ajax_required, login_required, staff_member_required
from .base import BaseSelectableTestCase, SimpleModelLookup

__all__ = (
    "AjaxRequiredLookupTestCase",
    "LoginRequiredLookupTestCase",
    "StaffRequiredLookupTestCase",
)


class AjaxRequiredLookupTestCase(BaseSelectableTestCase):
    def setUp(self):
        self.lookup = ajax_required(SimpleModelLookup)()

    def test_ajax_call(self):
        "Ajax call should yield a successful response."
        request = Mock(headers={"x-requested-with": "XMLHttpRequest"})
        response = self.lookup.results(request)
        self.assertTrue(response.status_code, 200)

    def test_non_ajax_call(self):
        "Non-Ajax call should yield a bad request response."
        request = Mock()
        response = self.lookup.results(request)
        self.assertEqual(response.status_code, 400)


class LoginRequiredLookupTestCase(BaseSelectableTestCase):
    def setUp(self):
        self.lookup = login_required(SimpleModelLookup)()

    def test_authenicated_call(self):
        "Authenicated call should yield a successful response."
        request = Mock()
        user = Mock()
        user.is_authenticated = True
        request.user = user
        response = self.lookup.results(request)
        self.assertTrue(response.status_code, 200)

    def test_non_authenicated_call(self):
        "Non-Authenicated call should yield an unauthorized response."
        request = Mock()
        user = Mock()
        user.is_authenticated = False
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
        user.is_authenticated = True
        user.is_staff = True
        request.user = user
        response = self.lookup.results(request)
        self.assertTrue(response.status_code, 200)

    def test_authenicated_but_not_staff(self):
        "Authenicated but non staff call should yield a forbidden response."
        request = Mock()
        user = Mock()
        user.is_authenticated = True
        user.is_staff = False
        request.user = user
        response = self.lookup.results(request)
        self.assertTrue(response.status_code, 403)

    def test_non_authenicated_call(self):
        "Non-Authenicated call should yield an unauthorized response."
        request = Mock()
        user = Mock()
        user.is_authenticated = False
        user.is_staff = False
        request.user = user
        response = self.lookup.results(request)
        self.assertEqual(response.status_code, 401)
