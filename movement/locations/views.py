from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

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
        Given a list of Location ids return the basic info for that list
            @params Ids of coords
            @example localhost:8000/api/v1/locations?ids=1,2,3,4
            
        """
        try:
            ids = [ int(id) for id in request.query_params.get('ids', '').split(',') ]
            # ref: https://docs.djangoproject.com/en/dev/ref/models/querysets/#in
            locations = Location.objects.filter( id__in=ids )
            return Response( [ { 'id': loc.id, 
                                 'name': loc.name, 
                                 'lat': loc.lat, 
                                 'lng': loc.lng,
                                 'total_visits': loc.total_visits } for loc in locations ] )
            
        except Exception as e:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )

    def put(self, request, format=None):
        """
        Allow a user to say they did not visit these coords 
        """
        loc_id = request.data.get('id', None)
        if loc_id:
            try:
                loc = Location.objects.get(id=loc_id)
                loc.total_visits = max( loc.total_visits - 1, 0 )
                loc.save( )
                return Response( {}, status=status.HTTP_200_OK )
            except ObjectDoesNotExist:
                return Response( {}, status=status.HTTP_404_NOT_FOUND ) 
        else:
            return Response( {}, status=status.HTTP_400_BAD_REQUEST )
    
    def post(self, request, format=None):
        """
        """
        serializer = LocationSerializer( data=request.data )
        if serializer.is_valid():
            
            loc, created = Location.objects.get_or_create( lat=serializer.data.get('lat'), 
                                                           lng=serializer.data.get('lng') )
            if created:
                # this should be done as a celery task asynchronously but we will
                # keep it synchronous for now
                geoInfo = geoSearch( loc.lat, loc.lng )
                if geoInfo is None:
                    # bad coords or we didnt find anything, so dump the point
                    # TODO: think more about how to handle this
                    loc.delete()
                    return Response( { 'reason': 'We could not translate the venue' }, status=status.HTTP_400_BAD_REQUEST )
                    
                loc.name = geoInfo.get('name')
                # TODO handle Location model use of category.
                # prob should be a many to many with a Category model
            
            # increment the total visits
            # TODO: This needs to be more robust so that 
            # we can keep track of visits on a per cohort basis.
            # ie. Cohort01 total_visits was 12 while Cohort02 total_visits was 2
            # same should apply to total_reveals, altough that is more simple
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


class LocationRevealAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    def get(self, request, format=None):
        """
        Get a list of other users who have revealed themselves for the venue
        that are in your cohort
        """
        pass

    def post(self, request, format=None):
        """
        Reveal that the user has been here
        """
        pass








