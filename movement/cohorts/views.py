from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Account
from .serializers import AccountSerializer, CohortSerializer, DeviceIDSerializer

class AccountCreationAPIHandler(APIView):
    def post(self, request, format=None):
        """
        Create a new user object
        """
        serializer = AccountSerializer( data=request.data )
        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.data.get('username'), 
                serializer.data.get('email'),
                serializer.data.get('password')
            )
            Account.objects.create(user=user, device_token=serializer.data.get('device_token'))
            return Response( {  }, status=status.HTTP_201_CREATED )
        else:
            print serializer.errors
            return Response( { 'msg': 'Please provide a valid email and password of at least 7 characters' }, 
                status=status.HTTP_400_BAD_REQUEST )


class AccountDeviceTokenAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        """
        Associate a device id with an account
        """
        serializer = DeviceIDSerializer( data=request.data )
        if serializer.is_valid():
            request.user.account.device_token = serializer.data.get('device_token')
            request.user.account.save()
            return Response( {  }, status=status.HTTP_200_OK )
        else:
            print serializer.errors
            return Response( {  }, 
                status=status.HTTP_400_BAD_REQUEST )
        


class CohortListCreateAPIHandler(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
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
            if Group.objects.filter( name=serializer.data.get('name').lower() ).exists( ):
                obj = Group.objects.get( name=serializer.data.get('name').lower() ) # we lowercase groups to avoid user error    
                # check if user belongs to cohort and if they don't add them to the cohort
                obj.user_set.add( request.user )
                return Response( { 'id': obj.id, 'name': obj.name }, status=status.HTTP_200_OK )
            else:
                return Response( { }, status=status.HTTP_404_NOT_FOUND )
        else:
            return Response( { }, status=status.HTTP_400_BAD_REQUEST )
