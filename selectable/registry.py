from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.utils.module_loading import autodiscover_modules

from selectable.base import LookupBase
from selectable.exceptions import (LookupAlreadyRegistered, LookupNotRegistered,
                                    LookupInvalid)


def _get_query_decorator(get_query_mtd, parent_entity_name):
    """
    This decorator is added on the form's lookup get_query method when the form 
    is registred in ChainedFormRegistry by the 'chained_field' decorator
    """

    def get_query(self, request, term):
        """
        Lookup get_query method.
        """
        results = get_query_mtd( self, request, term)
        parent_entity = request.GET.get(parent_entity_name, '')
        if parent_entity:
            results = results.filter(**{parent_entity_name:parent_entity})
        return results

    return get_query


class ChainedFormRegistry(object):
    """
    Decorate get_query lookup method and return chained field to templatetag
    in order to generate JavaScript code. You must not use this class dirrectly
    but use the chained_field decorator
    """

    def __init__(self):
        self._registry = {}
        
    def register(self, form, field_1, field_2):
        """
        Called when chained_field(field_1, field_2) decorator is used on the form class.
        """
        for field in (field_1, field_2):
            if not form.base_fields.has_key(field):
                raise ValueError("class '{}' has not field '{}'".format(form, field))

        lookup_class = form.base_fields.get(field_1).lookup_class
        lookup_class.get_query = _get_query_decorator(lookup_class.get_query, field_2)
        self._registry[form] = (field_1, field_2)

    def get(self, form_instance):
        """
        Return two chained fields in tuple or (None, None) tuple.
        """
        return self._registry.get(type(form_instance), (None, None))
        

ChainedFormRegistry = ChainedFormRegistry()


def chained_field(field_1, field_2):
    """
    Decorator for Form class to declare the dependency between two fields.
    field_1 is week entity of field_2.
    """
    def init(cls):
        ChainedFormRegistry.register(cls, field_1, field_2)
        return cls
    return init


class LookupRegistry(object):

    def __init__(self):
        self._registry = {}

    def validate(self, lookup):
        if not issubclass(lookup, LookupBase):
            raise LookupInvalid('Registered lookups must inherit from the LookupBase class')

    def register(self, lookup):
        self.validate(lookup)
        name = force_text(lookup.name())
        if name in self._registry:
            raise LookupAlreadyRegistered('The name %s is already registered' % name)
        self._registry[name] = lookup

    def unregister(self, lookup):
        self.validate(lookup)
        name = force_text(lookup.name())
        if name not in self._registry:
           raise LookupNotRegistered('The name %s is not registered' % name)
        del self._registry[name]

    def get(self, key):
        return self._registry.get(key, None)


registry = LookupRegistry()


def autodiscover():
    # Attempt to import the app's lookups module.
    autodiscover_modules('lookups', register_to=registry)
