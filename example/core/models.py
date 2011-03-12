from django.contrib import admin
from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


admin.site.register(Fruit)
