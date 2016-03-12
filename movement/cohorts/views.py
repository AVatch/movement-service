from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CohortSerializer

class CohortListCreateAPIHandler(APIView):
    def post(self, request, format=None):
        """
        Create a cohort obj or return the id if it exists.
        Also adds the user to the cohort. 
        Cohorts are simply the default Django Group object for now.
            @requires: token authentication
            @reference: https://docs.djangoproject.com/en/1.9/ref/contrib/auth/#django.contrib.auth.models.Group
        """

        serializer = CohortSerializer(data=request.data)
        if serializer.is_valid():
            obj, created = Group.objects.get_or_create( name=serializer.data.get('name').lower() )
            return Response( { 'id': obj.id }, status=status.HTTP_201_CREATED )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )

