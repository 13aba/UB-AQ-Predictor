from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import *

class PollutantList(generics.ListCreateAPIView):
    queryset = Pollutants.objects.all()
    serializer_class = PollutantSerializer

class LocationList(generics.ListCreateAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer

class MeasurementList(generics.ListCreateAPIView):
    queryset = Measurements.objects.all()
    serializer_class = MeasurementSerializer
    filterset_class = MeasurementFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.query_params.get('location')
        pollutant = self.request.query_params.get('pollutant')
        time_min = self.request.query_params.get('time_min')
        time_max = self.request.query_params.get('time_max')

        # Require at least one filter param
        if not any([location, pollutant, time_min, time_max]):
            return Measurements.objects.none()  #

        return queryset

class TemperatureList(generics.ListCreateAPIView):
    queryset = Temperatures.objects.all()
    serializer_class = TemperatureSerializer

