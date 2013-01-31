from __future__ import unicode_literals

from django.http import HttpResponse, Http404

from selectable.registry import registry


def get_lookup(request, lookup_name):

    lookup_cls = registry.get(lookup_name)
    if lookup_cls is None:
        raise Http404('Lookup %s not found' % lookup_name)

    lookup = lookup_cls()
    return lookup.results(request)

