from rest_framework import serializers
from .models import *

class PollutantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pollutants
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'

class MeasurementSerializer(serializers.ModelSerializer):

    #Show pollutant and locaiton name instead of their id
    locations = serializers.CharField(source='location.name')
    pollutant = serializers.CharField(source='pollutant.name')

    class Meta:
        model = Measurements
        fields = '__all__'

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperatures
        fields = '__all__'
