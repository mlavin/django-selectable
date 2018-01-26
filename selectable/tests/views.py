from django.http import HttpResponseNotFound, HttpResponseServerError


def test_404(request, *args, **kwargs):
    return HttpResponseNotFound()


def test_500(request, *args, **kwargs):
    return HttpResponseServerError()
