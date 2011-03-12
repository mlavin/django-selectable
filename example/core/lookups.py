from selectable.base import ModelLookup
from selectable.registry import registry

from example.core.models import Fruit


class FruitLookup(ModelLookup):
    model = Fruit
    search_field = 'name__icontains'


registry.register(FruitLookup)

