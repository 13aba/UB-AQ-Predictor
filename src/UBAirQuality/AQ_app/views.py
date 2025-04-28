from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
import os
import numpy as np
from datetime import timedelta
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

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

def graph_page(request):
    # Renders the template with dropdowns and Plotly graph
    return render(request, 'air_quality.html')


def predict(request):
    prediction = None
    selected_location = None
    selected_pollutant = None
    future_dates = None
    prediction_data = None

    locations = Locations.objects.all()
    pollutants = Pollutants.objects.all()

    if request.method == 'POST':
        location_id = request.POST.get('location')
        pollutant_id = request.POST.get('pollutant')

        selected_location = Locations.objects.get(id=location_id)
        selected_pollutant = Pollutants.objects.get(id=pollutant_id)

        # Prepare model filename
        model_name = f"{selected_location.name.replace(' ', '_')}_{selected_pollutant.name}.keras"
        model_path = os.path.join(os.path.dirname(__file__), 'models', model_name)
        model_path = os.path.abspath(model_path)  

        print(model_path)

        if os.path.exists(model_path):
            model = load_model(model_path)

            # Get last 30 days of data
            qs = Measurements.objects.filter(
                location=selected_location,
                pollutant=selected_pollutant
            ).order_by('-date')[:30]

           
            values = np.array(list(qs.values_list('value', flat=True)))
            values = values[::-1] 
            dates = np.array(list(qs.values_list('date', flat=True)))
            latest_day = dates[0]

            #Date for the predictions
            future_dates = [latest_day+ timedelta(days=i) for i in range(1, 8)]


            # Normalize values
            scaler = MinMaxScaler()
            values_scaled = scaler.fit_transform(values.reshape(-1, 1))

            # Reshape for LSTM
            input_seq = values_scaled.reshape((1, 30, 1))

            # Predict
            pred_scaled = model.predict(input_seq)

            # Inverse scale prediction
            pred = scaler.inverse_transform(pred_scaled)[0]

            # Round predictions
            prediction = [round(p, 2) for p in pred]
        else:
            prediction_data = "Model not found."

    # Zip future dates and prediction values together
    if(future_dates):
        prediction_data = list(zip(future_dates, prediction))

    return render(request, 'predict.html', {
        'locations': locations,
        'pollutants': pollutants,
        'prediction_data': prediction_data,
        'selected_location': selected_location,
        'selected_pollutant': selected_pollutant,
    })
