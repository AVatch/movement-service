from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .geoservice import geoSearch
from .models import Location, CohortAssociation, UserReveal
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
                                 'total_reveals': loc.get_total_reveals( ),
                                 'total_visits': loc.get_total_visits( ) 
                               } for loc in locations ] )
            
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
                # decrement the total visits
                for cohort in request.user.groups.all():
                    cohort_association = CohortAssociation.objects.get( cohort=cohort,
                                                                        location=loc )
                    cohort_association.total_visits = max( cohort_association.total_visits - 1, 0 )
                    cohort_association.save()

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
        
            geoInfo = geoSearch( serializer.data.get('lat'), serializer.data.get('lng') )
            if geoInfo is None:
                # bad coords or we didnt find anything, so dump the point
                # TODO: think more about how to handle this
                return Response( { 'reason': 'We could not translate the venue' }, status=status.HTTP_400_BAD_REQUEST )
            
            checkbyName = Location.objects.filter(name=geoInfo.get('name'))
            if checkbyName:
                # venue by name exists
                loc = checkbyName[0]
            else:
                # venue by name is not registered so register it
                loc = Location.objects.create( lat=serializer.data.get('lat'), 
                                               lng=serializer.data.get('lng'),
                                               name=geoInfo.get('name') )
            
            # increment the total visits
            for cohort in request.user.groups.all():
                cohort_association, created = CohortAssociation.objects.get_or_create( cohort=cohort,
                                                                                       location=loc )
                cohort_association.total_visits += 1
                cohort_association.save()

            # commit the changes
            loc.save()
        
            return Response( { 'id': loc.id }, status=status.HTTP_201_CREATED )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )


class LocationRevealAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """
        Get a list of other users who have revealed themselves for the venue
        that are in your cohort
        """
        loc = self.get_object(pk)
        
        # first lets ensure the user has already revealed themselves
        try:    
            reveal = UserReveal.objects.get( user=request.user, location=loc )
            
            # find the cohort intersection between the requester and the locaiton venues
            cohort_intersection = set( request.user.groups.all() ).intersection( [ cohort_association.cohort for cohort_association in CohortAssociation.objects.filter( location=loc ) ] ) 
       
            response = []
            user_reveals = UserReveal.objects.filter( location=loc )     
            for cohort in cohort_intersection:                
                # get the users that belong to this cohort and have revealed themselves
                revealed_users = []
                for user_reveal in user_reveals:
                    if cohort in user_reveal.user.groups.all():
                        revealed_users.append({
                            'username': user_reveal.user.username
                        })
                
                response.append({
                    'cohort': {
                        'id': cohort.id,
                        'name': cohort.name
                    },
                    'revealed_users': revealed_users
                })
        
            return Response( response, status=status.HTTP_200_OK )
        except Exception as e:
            print e
            return Response( { 'reason': 'User needs to first reveal themselves before getting other users' }, status=status.HTTP_400_BAD_REQUEST )
    
    def post(self, request, pk, format=None):
        """
        Reveal that the user has been here
        """
        
        print "Hello there"
        print request.auth
        
        if request.auth:
            loc = self.get_object(pk)
            reveal, created = UserReveal.objects.get_or_create( user=request.user, location=loc )
            return Response( { }, status=status.HTTP_200_OK )
        else:
            return Response( { }, status=status.HTTP_401_UNAUTHORIZED )
