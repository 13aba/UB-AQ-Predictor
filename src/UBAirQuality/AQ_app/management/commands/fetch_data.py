from django.core.management.base import BaseCommand
from AQ_app.models import Measurements, Pollutants, Locations
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetches air quality data and saves to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data fetch...")

        try:

            location = Locations.objects.get(name="US Embassy")
            pollutant = Pollutants.objects.get(name="pm25")
            
            #Dummy data
            new_measurement = Measurements.objects.create(
                location=location,
                pollutant=pollutant,
                date=datetime.today().date(),
                value=42.5  
            )

            self.stdout.write(self.style.SUCCESS(f"Saved new measurement"))
            
        except Locations.DoesNotExist:
            self.stderr.write("Location not found.")
        except Pollutants.DoesNotExist:
            self.stderr.write("Pollutant not found.")
        except Exception as e:
            self.stderr.write(f"Unexpected error: {e}")