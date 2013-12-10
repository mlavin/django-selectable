from django.http import HttpResponseNotFound, HttpResponseServerError

def test_404(request):
    return HttpResponseNotFound()


def test_500(request):
    return HttpResponseServerError()
