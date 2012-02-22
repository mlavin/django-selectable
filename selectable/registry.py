from django.utils.encoding import force_unicode

from selectable.base import LookupBase, ModelLookup
from selectable.exceptions import (LookupAlreadyRegistered, LookupNotRegistered,
                                    LookupInvalid)


class LookupRegistry(object):

    def __init__(self):
        self._registry = {}

    def validate(self, lookup):
        if not issubclass(lookup, LookupBase):
            raise LookupInvalid(u'Registered lookups must inherit from the LookupBase class')
        if issubclass(lookup, ModelLookup) and getattr(lookup, 'search_field', None):
            import warnings
            warnings.warn(
                u"ModelLookup.search_field is deprecated; Use ModelLookup.search_fields instead.", 
                DeprecationWarning
            )

    def register(self, lookup):

        self.validate(lookup)

        name = force_unicode(lookup.name())

        if name in self._registry:
            raise LookupAlreadyRegistered(u'The name %s is already registered' % name)
        self._registry[name] = lookup

    def unregister(self, lookup):

        self.validate(lookup)
    
        name = force_unicode(lookup.name())

        if name not in self._registry:
           raise LookupNotRegistered(u'The name %s is not registered' % name)
    
        del self._registry[name]

    def get(self, key):
        return self._registry.get(key, None)


registry = LookupRegistry()


def autodiscover():

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's lookups module.
        try:
            before_import_registry = copy.copy(registry._registry)
            import_module('%s.lookups' % app)
        except:
            registry._registry = before_import_registry

            if module_has_submodule(mod, 'lookups'):
                raise

