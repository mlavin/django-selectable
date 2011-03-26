from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Farm(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='farms')
    fruit = models.ManyToManyField(Fruit)

