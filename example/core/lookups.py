from django.contrib.auth.models import User

from selectable.base import ModelLookup
from selectable.registry import registry

from example.core.models import Fruit


class FruitLookup(ModelLookup):
    model = Fruit
    search_field = 'name__icontains'


registry.register(FruitLookup)


class OwnerLookup(ModelLookup):
    model = User
    search_field = 'username__icontains'


registry.register(OwnerLookup)
