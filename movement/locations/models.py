from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class Location(models.Model):
    name = models.CharField(max_length=140, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()

    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s <%s,%s>' % ( self.name, str(self.lat), str(self.lng) )
    
    def get_total_visits(self):
        return sum( cohort.total_visits for cohort in self.cohortassociation_set.all() )
    
    def get_total_reveals(self):
        return self.userreveal_set.all().count()


class CohortAssociation(models.Model):
    cohort = models.ForeignKey(Group)
    location = models.ForeignKey(Location)
    
    total_visits = models.IntegerField(default=0)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)


class UserReveal(models.Model):
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
