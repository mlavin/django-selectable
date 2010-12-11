from django.core.serializers import json
from django.http import HttpResponse, Http404
from django.utils import simplejson

from selectable.registry import registry


def get_lookup(request, lookup_name):

    lookup_cls = registry.get(lookup_name)
    if lookup_cls is None:
        raise Http404(u'Lookup %s not found' % lookup_name)

    lookup = lookup_cls()
    raw_data = lookup.get_query(request)
    data = []
    for item in raw_data:
        data.append(lookup.format_item(item))

    content = simplejson.dumps(data, cls=json.DjangoJSONEncoder, ensure_ascii=False)
    return HttpResponse(content, content_type='application/json')

