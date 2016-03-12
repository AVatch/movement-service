from rest_framework import serializers
from .geoservice import geoSearch
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ('associated_cohorts', 'revealed_users')