# This scripts wipes every data on the backend database and create new one from the csv files in the data folder



import sys
import os
import pandas as pd
import numpy as np
import django

# Getting path to maib folder path using dirname since main is three folder from this script
app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(app_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UBAirQuality.settings")
django.setup()

#import django models
from AQ_app.models import *

#Delete all previous data in the models
Pollutants.objects.all().delete()
Temperatures.objects.all().delete()
Measurements.objects.all().delete()
Locations.objects.all().delete()

#Read all csv data
df_embassy = pd.read_csv("../../../../data/ulaanbaatar-us embassy-air-quality.csv")
df_naran = pd.read_csv("../../../../data/urgakh-naran-air-quality.csv")
df_100 = pd.read_csv("../../../../data/100-ail-air-quality.csv")
df_misheel = pd.read_csv("../../../../data/misheel-expo-air-quality.csv")

#Data in one list
dataframes = [df_embassy, df_naran, df_100, df_misheel]
pollutants = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']

#Location data
location_data = [
    {"name": "US Embassy", "latitude": 47.9284, "longitude": 106.93021, "district": "Sukhbaatar"},
    {"name": "Urgakh Naran", "latitude": 47.8744, "longitude": 107.1137, "district": "Bayanzurkh"},
    {"name": "100 Ail", "latitude": 47.9319, "longitude": 106.9278, "district": "Sukhbaatar"},
    {"name": "Misheel Expo", "latitude": 47.8939, "longitude": 106.8840, "district": "Khan Uul"},
]

#Pollutant data
pollutant_data = [
    {"name": "pm25", "units": "µg/m³", "description": "Fine particulate matter"},
    {"name": "pm10", "units": "µg/m³", "description": "Coarse particulate matter"},
    {"name": "o3", "units": "ppb", "description": "Ozone"},
    {"name": "no2", "units": "ppb", "description": "Nitrogen Dioxide"},
    {"name": "so2", "units": "ppb", "description": "Sulfur Dioxide"},
    {"name": "co", "units": "ppb", "description": "Carbon Monoxide"},
]

# Create Locations
location_objects = {loc["name"]: Locations.objects.create(**loc) for loc in location_data}

# Create Pollutants
pollutant_objects = {p["name"]: Pollutants.objects.create(**p) for p in pollutant_data}


#Data cleaner function
def data_cleaner(df):
    #Remove the empty spaces from the columns
    df.columns = df.columns.str.strip()
    #Change empty data into Nan
    df = df.replace(to_replace = " ", value=np.nan)
    #Change dates to same format
    df['date'] = pd.to_datetime(df['date'])
    #Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    #Remove rows with only date data
    df = df.dropna(subset=pollutants, how='all')
    
    for col in pollutants:
        #Ensure data is in float format
        df[col] = pd.to_numeric(df[col], errors='coerce')
        #If data is more than 5 times of last 14 days median replace with NaN
        df.loc[df[col] > df[col].rolling(14, min_periods=2).median().shift(1) * 5, col] = np.nan
        #Fill the missing data with rolling median
        df[col] = df[col].fillna(df[col].rolling(7, min_periods=1).median())

    
    return df

# Clean and Process Data
for df, location in zip(dataframes, location_objects.values()):
    df_clean = data_cleaner(df)

    measurement_entries = []
    for _, row in df_clean.iterrows():
        for pollutant_name in ["pm25", "pm10", "o3", "no2", "so2", "co"]:
            if pd.notna(row[pollutant_name]):
                measurement_entries.append(
                    Measurements(
                        location=location,
                        pollutant=pollutant_objects[pollutant_name],
                        date=row["date"],
                        value=row[pollutant_name]
                    )
                )

    # Bulk insert measurements for efficiency
    Measurements.objects.bulk_create(measurement_entries)
