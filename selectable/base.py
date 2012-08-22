"Base classes for lookup creation."

import operator
import re

#from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.db.models import Q
from django.utils import simplejson as json
from django.utils.encoding import smart_unicode
from django.utils.html import conditional_escape
#from django.utils.translation import ugettext as _

from selectable.forms import BaseLookupForm
from selectable.forms.base import DEFAULT_LIMIT as MAX_LIMIT


__all__ = (
    'LookupBase',
    'ModelLookup',
)


class LookupBase(object):
    "Base class for all django-selectable lookups."

    form = BaseLookupForm
    max_limit = MAX_LIMIT

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
            'id': conditional_escape(self.get_item_id(item)),
            'value': conditional_escape(self.get_item_value(item)),
            'label': conditional_escape(self.get_item_label(item))
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
        results = {}
        form = self.form(request.GET)
        if form.is_valid():

            options = self._get_options(form)
            term, limit = options['term'], options['limit']
            raw_data = self.get_query(request, term)
            page_data = self.paginate_results(request, raw_data, limit)
            results = self.format_results(page_data, options)

        content = self.get_content(results)
        return self.get_response(content, 'application/json')

    def _get_options(self, valid_form):
        '''
        Returns a dictionary of options from a valid lookup form instance.
        `term` and `limit` are required
        '''
        term = valid_form.cleaned_data.get('term', '')
        limit = valid_form.cleaned_data.get('limit', self.max_limit)

        # check if provided limit isn't bigger than max_limit
        if limit and self.max_limit and limit > self.max_limit:
            limit = self.max_limit

        return {'term' : term, 'limit' : limit}

    def format_results(self, page_data, options):
        '''
        Returns a python structure that later gets serialized.
        page_data
            list of objects that where queried
        options
            a dictionary of the given options
        '''
        results = {}
        meta = options.copy()

        if page_data and hasattr(page_data, 'has_next') and page_data.has_next():
            meta.update( {
                'next_page': page_data.next_page_number(),
            })
        if page_data and hasattr(page_data, 'has_previous') and page_data.has_previous():
            meta.update( {
                'prev_page': page_data.previous_page_number(),
            })

        data = []
        if page_data and hasattr(page_data, 'object_list'):
            for item in page_data.object_list:
                data.append(self.format_item(item))

        results['data'] = data
        results['meta'] = meta

        return results

    def get_content(self, results):
        '''
        Returns serialized results for sending via http.
        '''
        return json.dumps(results, cls=DjangoJSONEncoder, ensure_ascii=False)

    def get_response(self, content, content_type='application/json'):
        '''
        Returns a HttpResponse with the given content and content_type.
        '''
        return HttpResponse(content, content_type=content_type)


class ModelLookup(LookupBase):
    "Lookup class for easily defining lookups based on Django models."

    model = None
    filters = {}
    search_fields = ()

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
