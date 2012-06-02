"Decorators for additional lookup functionality."

from functools import wraps

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden


__all__ = (
    'ajax_required',
    'login_required',
    'staff_member_required',
)


def results_decorator(func):
    """
    Helper for constructing simple decorators around Lookup.results.

    func is a function which takes a request as the first parameter. If func
    returns an HttpReponse it is returned otherwise the original Lookup.results
    is returned.
    """
    # Wrap function to maintian the original doc string, etc
    @wraps(func)
    def decorator(lookup_cls):
        # Construct a class decorator from the original function
        original = lookup_cls.results
        def inner(self, request):
            # Wrap lookup_cls.results by first calling func and checking the result
            result = func(request)
            if isinstance(result, HttpResponse):
                return result
            return original(self, request)
        # Replace original lookup_cls.results with wrapped version
        lookup_cls.results = inner
        return lookup_cls
    # Return the constructed decorator
    return decorator


@results_decorator
def ajax_required(request):    
    "Lookup decorator to require AJAX calls to the lookup view."
    if not request.is_ajax():
        return HttpResponseBadRequest()


@results_decorator
def login_required(request):
    "Lookup decorator to require the user to be authenticated."
    user = getattr(request, 'user', None)
    if user is None or not user.is_authenticated():
        return HttpResponse(status=401) # Unauthorized


@results_decorator
def staff_member_required(request):
    "Lookup decorator to require the user is a staff member."
    user = getattr(request, 'user', None)
    if user is None or not user.is_authenticated():
        return HttpResponse(status=401) # Unauthorized
    elif not user.is_staff:
        return HttpResponseForbidden()
