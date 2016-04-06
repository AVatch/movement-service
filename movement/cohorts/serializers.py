from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=80) 
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(max_length=80)
    device_token = serializers.CharField(max_length=500)

class CohortSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=80) 

