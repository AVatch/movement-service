from rest_framework import serializers


class CohortSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=80) 

