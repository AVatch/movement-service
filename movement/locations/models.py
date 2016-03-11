from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .geoservice import geoSearch

class LocationManager(models.Manager):
    def create_location(self, *args, **kwargs):
        """
        ref: https://docs.djangoproject.com/en/1.9/ref/models/instances/#django.db.models.Model.save
        """
        geoInfo = geoSearch(
            kwargs.get('lat'),
            kwargs.get('lng')
        )

        location = self.create(
            name = geoInfo.get('name'),
            lat = kwargs.get('lat'),
            lng = kwargs.get('lng')
        )
        
        return location

class Location(models.Model):
    name = models.CharField(max_length=140)
    lat = models.FloatField()
    lng = models.FloatField()
    
    total_visits = models.IntegerField(default=0)
    total_reveals = models.IntegerField(default=0)
    
    revealed_users = models.ManyToManyField(User)
    associated_cohorts = models.ManyToManyField(Group)

    def __str__(self):
        return '%s<%s,%s>' % ( self.name, str(self.lat), str(self.lng) )
    
    objects = LocationManager()