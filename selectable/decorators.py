"Decorators for additional lookup functionality."

from functools import wraps

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden


__all__ = (
    'ajax_required',
    'login_required',
    'staff_member_required',
)


def ajax_required(lookup_cls):
    "Lookup decorator to require AJAX calls to the lookup view."

    func = lookup_cls.results

    @wraps(func)
    def wrapper(self, request):
        "Wrapped results function."
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return func(self, request)

    lookup_cls.results = wrapper
    return lookup_cls


def login_required(lookup_cls):
    "Lookup decorator to require the user to be authenticated."

    func = lookup_cls.results

    @wraps(func)
    def wrapper(self, request):
        "Wrapped results function."
        user = getattr(request, 'user', None)
        if user is None or not user.is_authenticated():
            return HttpResponse(status=401) # Unauthorized
        return func(self, request)

    lookup_cls.results = wrapper
    return lookup_cls


def staff_member_required(lookup_cls):
    "Lookup decorator to require the user is a staff member."
    func = lookup_cls.results

    @wraps(func)
    def wrapper(self, request):
        "Wrapped results function."
        user = getattr(request, 'user', None)
        if user is None or not user.is_authenticated():
            return HttpResponse(status=401) # Unauthorized
        elif not user.is_staff:
            return HttpResponseForbidden()
        return func(self, request)

    lookup_cls.results = wrapper
    return lookup_cls
