from django.urls import path
from . import views

urlpatterns = [
    path('graph/', views.graph_page, name='aq_graph'),
    path('api/pollutants/', views.PollutantList.as_view(), name='pollutant-list'),
    path('api/locations/', views.LocationList.as_view(), name='location-list'),
    path('api/measurements/', views.MeasurementList.as_view(), name='measurement-list'),
    path('api/temperatures/', views.TemperatureList.as_view(), name='temperature-list'),
]
