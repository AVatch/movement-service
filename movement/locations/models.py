from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .geo_service import search as geo_search


class LocationCategory(models.Model):
    name = models.CharField(max_length=140)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s' % ( self.name, )
    
    def __unicode__(self):
        return '%s' % ( self.name, )


class LocationManager(models.Manager):
    def create_location(self, category_name, location_name, coords):
        loc_category, created = LocationCategory.objects.get_or_create(
            name = category_name
        )
        loc = self.create(
            name = location_name,
            lat = coords.get('lat'),
            lng = coords.get('lng')
        )
        loc.categories.add( loc_category )
        
        return loc   
                        
    def register_location(self, **validated_data):
        PRECISION = 10000 # to what precision do we store lat / lng values
        THRESHOLD = 10 # what error are we willing to accept for venue lat / lng
         
        loc_coords_query = self.filter( 
            lat = int( validated_data.get('lat') * PRECISION ), 
            lng = int( validated_data.get('lng') * PRECISION )
        )

        if loc_coords_query:
            return loc_coords_query[0]
        else:
            geo_search_results = geo_search(
                validated_data.get('lat'),
                validated_data.get('lng')
            )
            if geo_search_results is None:
                return None
            else:
                loc_name_query = self.filter(
                    name = geo_search_results.get('name')
                )
                
                if loc_name_query:
                    loc_candidate = loc_name_query[0]
                    if ( abs( abs(loc_candidate.lat) - abs( int( validated_data.get('lat') * PRECISION ) ) ) < THRESHOLD and 
                         abs( abs(loc_candidate.lng) - abs( int( validated_data.get('lng') * PRECISION ) ) ) < THRESHOLD ):
                        return loc_candidate
                    else:
                        return self.create_location( 
                            geo_search_results.get('category'),
                            geo_search_results.get('name'),
                            {
                                'lat': int( validated_data.get('lat') * PRECISION ),
                                'lng': int( validated_data.get('lng') * PRECISION )
                            }
                        )
                else:
                    return self.create_location( 
                            geo_search_results.get('category'),
                            geo_search_results.get('name'),
                            {
                                'lat': int( validated_data.get('lat') * PRECISION ),
                                'lng': int( validated_data.get('lng') * PRECISION )
                            }
                        )


class Location(models.Model):
    name = models.CharField(max_length=140, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    categories = models.ManyToManyField(LocationCategory, related_name='location_categories')
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    
    objects = LocationManager()

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
