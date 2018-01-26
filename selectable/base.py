"Base classes for lookup creation."
from __future__ import unicode_literals

import operator
import re
from functools import reduce

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q, Model
from django.utils.encoding import smart_text
from django.utils.html import conditional_escape
from django.utils.translation import ugettext as _

from selectable.forms import BaseLookupForm


__all__ = (
    'LookupBase',
    'ModelLookup',
)


class LookupBase(object):
    "Base class for all django-selectable lookups."

    form = BaseLookupForm
    response = JsonResponse

    def _name(cls):
        app_name = cls.__module__.split('.')[-2].lower()
        class_name = cls.__name__.lower()
        name = '%s-%s' % (app_name, class_name)
        return name
    name = classmethod(_name)

    def split_term(self, term):
        """
        Split searching term into array of subterms
        that will be searched separately.
        """
        return term.split()

    def _url(cls):
        return reverse('selectable-lookup', args=[cls.name()])
    url = classmethod(_url)

    def get_query(self, request, term):
        return []

    def get_item_label(self, item):
        return smart_text(item)

    def get_item_id(self, item):
        return smart_text(item)

    def get_item_value(self, item):
        return smart_text(item)

    def get_item(self, value):
        return value

    def create_item(self, value):
        raise NotImplemented()

    def format_item(self, item):
        "Construct result dictionary for the match item."
        result = {
            'id': self.get_item_id(item),
            'value': self.get_item_value(item),
            'label': self.get_item_label(item),
        }
        for key in settings.SELECTABLE_ESCAPED_KEYS:
            if key in result:
                result[key] = conditional_escape(result[key])
        return result

    def paginate_results(self, results, options):
        "Return a django.core.paginator.Page of results."
        limit = options.get('limit', settings.SELECTABLE_MAX_LIMIT)
        paginator = Paginator(results, limit)
        page = options.get('page', 1)
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)
        return results

    def results(self, request):
        "Match results to given term and return the serialized HttpResponse."
        results = {}
        form = self.form(request.GET)
        if form.is_valid():
            options = form.cleaned_data
            term = options.get('term', '')
            raw_data = self.get_query(request, term)
            results = self.format_results(raw_data, options)
        return self.response(results)

    def format_results(self, raw_data, options):
        '''
        Returns a python structure that later gets serialized.
        raw_data
            full list of objects matching the search term
        options
            a dictionary of the given options
        '''
        page_data = self.paginate_results(raw_data, options)
        results = {}
        meta = options.copy()
        meta['more'] = _('Show more results')
        if page_data and page_data.has_next():
            meta['next_page'] = page_data.next_page_number()
        if page_data and page_data.has_previous():
            meta['prev_page'] = page_data.previous_page_number()
        results['data'] = [self.format_item(item) for item in page_data.object_list]
        results['meta'] = meta
        return results


class ModelLookup(LookupBase):
    "Lookup class for easily defining lookups based on Django models."

    model = None
    filters = {}
    search_fields = ()

    def get_query(self, request, term):
        qs = self.get_queryset()
        if term:
            if self.search_fields:
                for t in self.split_term(term):
                    search_filters = []
                    for field in self.search_fields:
                        search_filters.append(Q(**{field: t}))
                    qs = qs.filter(reduce(operator.or_, search_filters))
        return qs

    def get_queryset(self):
        qs = self.model._default_manager.get_queryset()
        if self.filters:
            qs = qs.filter(**self.filters)
        return qs

    def get_item_id(self, item):
        return item.pk

    def get_item(self, value):
        item = None
        if value:
            value = value.pk if isinstance(value, Model) else value
            try:
                item = self.get_queryset().get(pk=value)
            except (ValueError, self.model.DoesNotExist):
                item = None
        return item

    def create_item(self, value):
        data = {}
        if self.search_fields:
            field_name = re.sub(r'__\w+$', '',  self.search_fields[0])
            if field_name:
                data = {field_name: value}
        return self.model(**data)
