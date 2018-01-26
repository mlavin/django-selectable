from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ..base import ModelLookup
from ..registry import registry


@python_2_unicode_compatible
class Thing(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


@python_2_unicode_compatible
class OtherThing(models.Model):
    name = models.CharField(max_length=100)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ManyThing(models.Model):
    name = models.CharField(max_length=100)
    things = models.ManyToManyField(Thing)

    def __str__(self):
        return self.name


class ThingLookup(ModelLookup):
    model = Thing
    search_fields = ('name__icontains', )


registry.register(ThingLookup)
