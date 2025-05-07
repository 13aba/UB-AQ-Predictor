from django.core.management.base import BaseCommand
from AQ_app.models import Measurements, Pollutants, Locations
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetches air quality data and saves to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data fetch...")

        #Agaar.mn url id to the name of the location
        station_map = {
            7: "Misheel Expo",
            10: "100 Ail",
            12: "Urgakh Naran",
            9: "US Embassy"
        }

        #Pollutant display order on the website
        pollutant_order = ["pm10", "pm25", "co", "so2", "no2"]

        try:
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)

            for station_id, location_name in station_map.items():
                url = f"http://agaar.mn/station/{station_id}"
                driver.get(url)

                try:
                    location = Locations.objects.get(name=location_name)
                except Locations.DoesNotExist:
                    self.stderr.write(f"Location not found: {location_name}")
                    continue

                all_class = driver.find_elements(By.CLASS_NAME, "col-xs-4")
                measurements = all_class[3:17:3]  

                for i, measurement in enumerate(measurements):
                    try:
                        value = float(measurement.text.strip())
                        pollutant_name = pollutant_order[i]
                        pollutant = Pollutants.objects.get(name=pollutant_name)

                        Measurements.objects.create(
                            location=location,
                            pollutant=pollutant,
                            date=datetime.today().date(),
                            value=value
                        )

                        self.stdout.write(self.style.SUCCESS(
                            f"Saved {pollutant_name.upper()} for {location_name}: {value}"
                        ))
                    except Pollutants.DoesNotExist:
                        self.stderr.write(f"Pollutant not found: {pollutant_name}")
                    except ValueError:
                        self.stderr.write(f"Invalid value for {pollutant_name} at {location_name}")
                    except Exception as e:
                        self.stderr.write(f"Error saving {pollutant_name} for {location_name}: {e}")

            driver.quit()
            self.stdout.write(self.style.SUCCESS("Data fetch complete."))

        except Exception as e:
            self.stderr.write(f"Unexpected error: {e}")