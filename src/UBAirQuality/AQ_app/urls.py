from django.urls import path
from . import views

urlpatterns = [
    path('pollutants/', views.PollutantList.as_view(), name='pollutant-list'),
    path('locations/', views.LocationList.as_view(), name='location-list'),
    path('measurements/', views.MeasurementList.as_view(), name='measurement-list'),
    path('temperatures/', views.TemperatureList.as_view(), name='temperature-list'),
]
