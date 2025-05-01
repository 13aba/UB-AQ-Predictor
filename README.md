#  Ulaanbaatar Air Quality Forecasting App

This project is a full-stack web application designed to monitor and forecast air quality in Ulaanbaatar, Mongolia. It allows users to visualize historical air quality data and predict the next 7 days of pollutant levels using LSTM (Long Short-Term Memory) models.

Users can choose a location and pollutant type, view interactive graphs of past data, and receive 7-day forecasts based on trained deep learning models.

---

##  Built With

- **Backend Framework**: Django, Django REST Framework  
- **Frontend**: HTML, JavaScript, Plotly.js  
- **Machine Learning**: Keras (TensorFlow backend), LSTM models  
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)  
- **Data Source**: CSV files from [AQICN](https://aqicn.org/city/ulaanbaatar/) and publicly available historical records  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/13aba/ub-aq-predictor.git
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Set up Django
```bash
python manage.py migrate
```
### 4. Populate the database from CSV files
```bash
python src/ubairquality/AQ_app/scripts/load_data.py
```
### 5. Run the development server
```bash
python manage.py runserver
```
---

## Usage

After starting the development server, the application is available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

-  **Historical Data**: Visit `/graph` to explore past air quality measurements by location and pollutant.
-  **Air Quality Prediction**: Go to `/predict` to generate 7-day forecasts using trained LSTM models.
-  **API Access**: Access structured JSON data through endpoints like `/api/locations/`, `/api/pollutants/`, and `/api/measurements/`.


