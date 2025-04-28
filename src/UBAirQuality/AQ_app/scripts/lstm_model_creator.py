import os, sys
import django
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import datetime

#Django setup
# Getting path to maib folder path using dirname since main is three folder from this script
app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(app_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UBAirQuality.settings')
django.setup()

#import django models
from AQ_app.models import * 

#Path to models folder
models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')

# Function to create sequence list and next value list of that sequence 
def create_sequences(data, seq_len):
    x, y = [], []
    for i in range(len(data) - seq_len):
        x.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(x), np.array(y)

#Create model for each location and pollutant combination
locations = Locations.objects.all()
pollutants = Pollutants.objects.all()

for pollutant in pollutants:
    for location in locations:
        print(f"Training for Location: {location}, Pollutant: {pollutant}")
         
        # Filter the measurements
        qs = Measurements.objects.filter(pollutant=pollutant, location=location).order_by('date')
        df = pd.DataFrame.from_records(qs.values('date', 'value'))

        # Normalize the 'value' column only
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(df[['value']])

        # Create sequence with 30 days window
        seq_len = 30
        x, y = create_sequences(data_scaled, seq_len)

        # Reshape x to (batch, time, features)
        x = x.reshape((x.shape[0], x.shape[1], 1))

        #Create test and train split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)

        #Create the model
        model = Sequential()
        #LSTM layers
        model.add(LSTM(64, return_sequences=True, input_shape=(seq_len, 1)))
        model.add(LSTM(64, return_sequences=False))

        #Final layer to predict the next weeks value
        model.add(Dense(7))
        model.compile(optimizer='adam', loss='mae')

        #Train to model
        training = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=20, batch_size=32)

        # Save model
        model_filename = f"{location.name.replace(' ', '_')}_{pollutant.name}.h5"
        model_path = os.path.join(models_dir, model_filename)
        model.save(model_path)