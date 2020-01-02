from django.db import models

from localflavor.us.models import USStateField


class Fruit(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Farm(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='farms', on_delete=models.CASCADE)
    fruit = models.ManyToManyField(Fruit)

    def __str__(self):
        return "%s's Farm: %s" % (self.owner.username, self.name)


class City(models.Model):
    name = models.CharField(max_length=200)
    state = USStateField()

    def __str__(self):
        return self.name
