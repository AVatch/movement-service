from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .geoservice import geoSearch
from .models import Location
from .serializers import LocationSerializer


class LocationListCreateAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    def get(self, request, format=None):
        """
        """
        return Response( { } )
    
    def post(self, request, format=None):
        """
        """
        authentication_classes = (SessionAuthentication, TokenAuthentication)
        serializer = LocationSerializer( data=request.data )
        if serializer.is_valid():
            
            loc, created = Location.objects.get_or_create( lat=serializer.data.get('lat'), 
                                                           lng=serializer.data.get('lng') )
            if created:
                # this should be done as a celery task asynchronously but we will
                # keep it synchronous for now
                geoInfo = geoSearch( loc.lat, loc.lng )
                
                loc.name = geoInfo.get('name')
                # TODO handle Location model use of category.
                # prob should be a many to many with a Category model
            
            # increment the total visits
            loc.total_visits += 1
            
            # add the cohort the user belongs in to the Location
            # associated cohorts
            for cohort in request.user.groups.all():
                loc.associated_cohorts.add( cohort )

            # commit the changes
            loc.save()
        
            return Response( { 'id': loc.id }, status=status.HTTP_201_CREATED )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )
