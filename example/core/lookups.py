from django.contrib.auth.models import User

from selectable.base import ModelLookup
from selectable.registry import registry

from example.core.models import Fruit, City


class FruitLookup(ModelLookup):
    model = Fruit
    search_fields = ('name__icontains', )

registry.register(FruitLookup)


class OwnerLookup(ModelLookup):
    model = User
    search_fields = ('username__icontains', )


registry.register(OwnerLookup)


class CityLookup(ModelLookup):
    model = City
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super(CityLookup, self).get_query(request, term)
        state = request.GET.get('state', '')
        if state:
            results = results.filter(state=state)
        return results

    def get_item_label(self, item):
        return u"%s, %s" % (item.name, item.state)


registry.register(CityLookup)
