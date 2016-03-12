from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .serializers import CohortSerializer

class CohortListCreateAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    def get(self, request, format=None):
        """
        Return a list of all the cohorts the user belongs to
        """
        return Response( [ { 'id': cohort.id, 'name': cohort.name } for cohort in request.user.groups.all() ], status=status.HTTP_200_OK )
        
    def post(self, request, format=None):
        """
        Create a cohort obj or return the id if it exists.
        Also adds the user to the cohort. 
        Cohorts are simply the default Django Group object for now.
            @reference: https://docs.djangoproject.com/en/1.9/ref/contrib/auth/#django.contrib.auth.models.Group
        """

        serializer = CohortSerializer( data=request.data )
        if serializer.is_valid():
            obj, created = Group.objects.get_or_create( name=serializer.data.get('name').lower() ) # we lowercase groups to avoid user error
            
            # check if user belongs to cohort and if they don't add them to the cohort
            obj.user_set.add( request.user )
            
            return Response( { 'id': obj.id }, status=status.HTTP_201_CREATED )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )
