import re
from django.core.urlresolvers import reverse
from django.core.serializers import json
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import smart_unicode


__all__ = (
    'LookupBase',
    'ModelLookup',
)


class LookupBase(object):

    def _name(cls):
        app_name = cls.__module__.split('.')[-2].lower()
        class_name = cls.__name__.lower()
        name = u'%s-%s' % (app_name, class_name)       
        return name
    name = classmethod(_name)

    def _url(cls):
        return reverse('selectable-lookup', args=[cls.name()])
    url = classmethod(_url)

    def get_query(self, request, term):
        return []

    def get_item_label(self, item):
        return smart_unicode(item)

    def get_item_id(self, item):
        return smart_unicode(item)

    def get_item_value(self, item):
        return smart_unicode(item)

    def get_item(self, value):
        return None

    def create_item(self, value):
        raise NotImplemented()

    def format_item(self, item):
         return {
            'id': self.get_item_id(item),
            'value': self.get_item_value(item),
            'label': self.get_item_label(item)
        }


    def results(self, request):
        term = request.GET.get('term', '')
        raw_data = self.get_query(request, term)
        data = []
        for item in raw_data:
            data.append(self.format_item(item))
        content = simplejson.dumps(data, cls=json.DjangoJSONEncoder, ensure_ascii=False)
        return HttpResponse(content, content_type='application/json')    


class ModelLookup(LookupBase):
    model = None
    filters = {}
    search_field = ''

    def get_query(self, request, term):
        qs = self.get_queryset()
        if term and self.search_field:
            qs = qs.filter(**{self.search_field: term})
        return qs

    def get_queryset(self):
        qs = self.model._default_manager.get_query_set()
        if self.filters:
            qs = qs.filter(**self.filters)
        return qs

    def get_item_id(self, item):
        return item.pk

    def get_item(self, value):
        item = None
        if value:
            try:
                item = self.get_queryset().filter(pk=value)[0]
            except IndexError:
                pass
        return item

    def create_item(self, value):
        data = {}
        if self.search_field:
            field_name = re.sub(r'__\w+$', '',  self.search_field)
            if field_name:
                data = {field_name: value}
        return self.model(**data)

