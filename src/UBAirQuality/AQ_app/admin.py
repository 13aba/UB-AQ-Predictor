from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Pollutants)
admin.site.register(Locations)
admin.site.register(Measurements)
admin.site.register(Temperatures)