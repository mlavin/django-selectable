import operator
import re

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson as json
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

from selectable.forms import BaseLookupForm


__all__ = (
    'LookupBase',
    'ModelLookup',
)


class LookupBase(object):
    form = BaseLookupForm

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
        return value

    def create_item(self, value):
        raise NotImplemented()

    def format_item(self, item):
         return {
            'id': self.get_item_id(item),
            'value': self.get_item_value(item),
            'label': self.get_item_label(item)
        }

    def paginate_results(self, request, results, limit):
        paginator = Paginator(results, limit)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)
        return results

    def results(self, request):
        data = []
        form = self.form(request.GET)
        if form.is_valid():
            term = form.cleaned_data.get('term', '')
            limit = form.cleaned_data.get('limit', None)
            raw_data = self.get_query(request, term)
            page_data = None      
            if limit:
                page_data = self.paginate_results(request, raw_data, limit)
                raw_data = page_data.object_list
            for item in raw_data:
                data.append(self.format_item(item))
            if page_data and hasattr(page_data, 'has_next') and page_data.has_next():
                data.append({
                    'id': '',
                    'value': '',
                    'label': _('Show more results'),
                    'page': page_data.next_page_number()
                })        
        content = json.dumps(data, cls=DjangoJSONEncoder, ensure_ascii=False)
        return HttpResponse(content, content_type='application/json')    


class ModelLookup(LookupBase):
    model = None
    filters = {}
    search_field = ''
    search_fields = ()

    def __init__(self):
        super(ModelLookup, self).__init__()
        if self.search_field and not self.search_fields:
            self.search_fields = (self.search_field, )

    def get_query(self, request, term):
        qs = self.get_queryset()
        if term:
            search_filters = []
            if self.search_fields:
                for field in self.search_fields:
                    search_filters.append(Q(**{field: term}))
            qs = qs.filter(reduce(operator.or_, search_filters))
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
        if self.search_fields:
            field_name = re.sub(r'__\w+$', '',  self.search_fields[0])
            if field_name:
                data = {field_name: value}
        return self.model(**data)

