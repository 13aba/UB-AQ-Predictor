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

