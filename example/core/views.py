from django.shortcuts import render_to_response
from django.template import RequestContext

from example.core.forms import FruitForm


def index(request):

    if request.method == 'POST':
        form = FruitForm(request.POST)
    else:
        form = FruitForm()

    return render_to_response('base.html', {'form': form}, context_instance=RequestContext(request))
