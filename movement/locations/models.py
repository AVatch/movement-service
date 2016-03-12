from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class Location(models.Model):
    name = models.CharField(max_length=140, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    
    total_visits = models.IntegerField(default=0)
    
    revealed_users = models.ManyToManyField(User, blank=True)
    associated_cohorts = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return '%s<%s,%s>' % ( self.name, str(self.lat), str(self.lng) )
