from django.utils.encoding import force_str
from django.utils.module_loading import autodiscover_modules

from selectable.base import LookupBase
from selectable.exceptions import (LookupAlreadyRegistered, LookupNotRegistered,
                                   LookupInvalid)


class LookupRegistry():

    def __init__(self):
        self._registry = {}

    def validate(self, lookup):
        if not issubclass(lookup, LookupBase):
            raise LookupInvalid('Registered lookups must inherit from the LookupBase class')

    def register(self, lookup):
        self.validate(lookup)
        name = force_str(lookup.name())
        if name in self._registry:
            raise LookupAlreadyRegistered('The name %s is already registered' % name)
        self._registry[name] = lookup

    def unregister(self, lookup):
        self.validate(lookup)
        name = force_str(lookup.name())
        if name not in self._registry:
            raise LookupNotRegistered('The name %s is not registered' % name)
        del self._registry[name]

    def get(self, key):
        return self._registry.get(key, None)


registry = LookupRegistry()


def autodiscover():
    # Attempt to import the app's lookups module.
    autodiscover_modules('lookups', register_to=registry)
