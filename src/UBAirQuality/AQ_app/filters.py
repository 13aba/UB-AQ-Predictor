import django_filters
from .models import Measurements

class MeasurementFilter(django_filters.FilterSet):
    time_min = django_filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    time_max = django_filters.DateTimeFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Measurements
        fields = {
            'location': ['exact'],
            'pollutant': ['exact'],
        }
