from django.db import models

# Create your models here.


class Pollutants(models.Model):
    name = models.CharField(max_length=30)
    units = models.CharField(max_length=30)
    description = models.CharField(max_length=30)

class Locations(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    district = models.CharField(max_length=30)

class Measurements(models.Model):
    pollutant = models.ForeignKey(Pollutants, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    date = models.DateField()

class Temperatures(models.Model):
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    date = models.DateField()
    temperature = models.FloatField()
    