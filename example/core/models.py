from __future__ import unicode_literals

from django.db import models
from django.utils.six import python_2_unicode_compatible

from localflavor.us.models import USStateField


@python_2_unicode_compatible
class Fruit(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Farm(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='farms', on_delete=models.CASCADE)
    fruit = models.ManyToManyField(Fruit)

    def __str__(self):
        return "%s's Farm: %s" % (self.owner.username, self.name)


@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(max_length=200)
    state = USStateField()

    def __str__(self):
        return self.name
