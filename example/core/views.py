from django.shortcuts import render_to_response
from django.template import RequestContext

from example.core.forms import FruitForm, ChainedForm, FarmFormset


def index(request):

    if request.method == 'POST':
        form = FruitForm(request.POST)
    else:
        if request.GET:
            form = FruitForm(initial=request.GET)
        else:
            form = FruitForm()

    return render_to_response('base.html', {'form': form}, context_instance=RequestContext(request))


def advanced(request):

    if request.method == 'POST':
        form = ChainedForm(request.POST)
    else:
        if request.GET:
            form = ChainedForm(initial=request.GET)
        else:
            form = ChainedForm()

    return render_to_response('advanced.html', {'form': form}, context_instance=RequestContext(request))


def formset(request):

    if request.method == 'POST':
        formset = FarmFormset(request.POST)
    else:
        if request.GET:
            formset = FarmFormset(initial=request.GET)
        else:
            formset = FarmFormset()

    return render_to_response('formset.html', {'formset': formset}, context_instance=RequestContext(request))
