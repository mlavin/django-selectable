from django.db import models

from selectable.base import ModelLookup
from selectable.registry import registry


class Thing(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class OtherThing(models.Model):
    name = models.CharField(max_length=100)
    thing = models.ForeignKey(Thing)

    def __unicode__(self):
        return self.name


class ThingLookup(ModelLookup):
    model = Thing
    search_fields = ('name__icontains', )


registry.register(ThingLookup)


from selectable.tests.base import *
from selectable.tests.fields import *
from selectable.tests.functests import *
from selectable.tests.forms import *
from selectable.tests.views import *
from selectable.tests.widgets import *
