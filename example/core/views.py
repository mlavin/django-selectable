import pprint

from django.shortcuts import render

from core.forms import FruitForm, ChainedForm, FarmFormset


def index(request):

    if request.method == 'POST':
        form = FruitForm(request.POST)
    else:
        if request.GET:
            form = FruitForm(initial=request.GET)
        else:
            form = FruitForm()

    raw_post = ''
    cleaned_data = ''
    if request.POST:
        raw_post = pprint.pformat(dict(request.POST))
        if form.is_valid():
            cleaned_data = pprint.pformat(getattr(form, 'cleaned_data', ''))

    context = {
        'cleaned_data': cleaned_data,
        'form': form,
        'raw_post': raw_post
    }
    return render(request, 'base.html', context)


def advanced(request):

    if request.method == 'POST':
        form = ChainedForm(request.POST)
    else:
        if request.GET:
            form = ChainedForm(initial=request.GET)
        else:
            form = ChainedForm()

    return render(request, 'advanced.html', {'form': form})


def formset(request):

    if request.method == 'POST':
        formset = FarmFormset(request.POST)
    else:
        if request.GET:
            formset = FarmFormset(initial=request.GET)
        else:
            formset = FarmFormset()

    return render(request, 'formset.html', {'formset': formset})
