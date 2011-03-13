from django.db import models

from selectable.base import ModelLookup
from selectable.registry import registry


class Thing(models.Model):
    name = models.CharField(max_length=100)


class ThingLookup(ModelLookup):
    model = Thing
    search_field = 'name__icontains'


registry.register(ThingLookup)


from selectable.tests.base import *
from selectable.tests.fields import *
from selectable.tests.views import *
from selectable.tests.widgets import *
