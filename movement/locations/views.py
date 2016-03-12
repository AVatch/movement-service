from rest_framework import generics

from .models import Location
from .serializers import LocationSerializer

class LocationListCreateAPIHandler(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    paginate_by = 100
    
    def perform_create(self, serializer):
        """
        see if this coord pair exists already, and only create
        if it does otherwise return the object
        """
        print self.request.data
        if Location.objects.filter(lat=self.request.data.get('lat')).filter(lng=self.request.data.get('lng')):
            print 'it exists'
        else:
            serializer.save()