from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
from datetime import datetime
import sys
import os

app = Flask(__name__)

# Handle PyInstaller paths
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

app.template_folder = os.path.join(base_path, 'templates')

# Serve manifest.json
@app.route('/manifest.json')
def manifest():
    return send_from_directory(base_path, 'manifest.json')

# Serve static files (icons)
@app.route('/static/<path:filename>')
def static_files(filename):
    static_folder = os.path.join(base_path, 'static')
    return send_from_directory(static_folder, filename)

def get_noaa_data(latitude, longitude):
    try:
        points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
        headers = {'User-Agent': 'WeatherApp'}
        points_response = requests.get(points_url, headers=headers, timeout=10)
        points_response.raise_for_status()
        points_data = points_response.json()
        
        forecast_url = points_data['properties']['forecast']
        forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        hourly_url = points_data['properties']['forecastHourly']
        hourly_response = requests.get(hourly_url, headers=headers, timeout=10)
        hourly_response.raise_for_status()
        hourly_data_raw = hourly_response.json()
        
        current_temp = forecast_data['properties']['periods'][0]['temperature']
        
        hourly_data = []
        for period in hourly_data_raw['properties']['periods'][:12]:
            time_str = datetime.fromisoformat(period['startTime'].replace('Z', '+00:00'))
            hour_label = time_str.strftime('%I%p').lstrip('0')
            hourly_data.append({
                'hour': hour_label,
                'temp': period['temperature']
            })
        
        return current_temp, hourly_data
    except Exception as e:
        print(f"NOAA API Error: {e}")
        return None, []

def get_openweather_data(latitude, longitude, api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['main']['temp']
    except Exception as e:
        print(f"OpenWeather API Error: {e}")
        return None

def get_weatherapi_data(latitude, longitude, api_key):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['current']['temp_f']
    except Exception as e:
        print(f"WeatherAPI Error: {e}")
        return None

def predict_temperature(temps):
    valid_temps = [t for t in temps if t is not None]
    if not valid_temps:
        return None
    return round(sum(valid_temps) / len(valid_temps), 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    openweather_key = data.get('openweather_key', '').strip()
    weatherapi_key = data.get('weatherapi_key', '').strip()
    
    if not latitude or not longitude:
        return jsonify({'error': 'Location required'}), 400
    
    noaa_temp, hourly_data = get_noaa_data(latitude, longitude)
    
    temps = []
    data_sources = []
    all_predictions = []
    
    if noaa_temp:
        temps.append(noaa_temp)
        data_sources.append("NOAA Weather Service")
        all_predictions.append(noaa_temp)
    
    if openweather_key:
        ow_temp = get_openweather_data(latitude, longitude, openweather_key)
        if ow_temp:
            temps.append(ow_temp)
            data_sources.append("OpenWeatherMap")
            all_predictions.append(ow_temp)
    
    if weatherapi_key:
        wa_temp = get_weatherapi_data(latitude, longitude, weatherapi_key)
        if wa_temp:
            temps.append(wa_temp)
            data_sources.append("WeatherAPI")
            all_predictions.append(wa_temp)
    
    prediction = predict_temperature(temps)
    
    if prediction is None:
        return jsonify({'error': 'Could not fetch weather data'}), 500
    
    return jsonify({
        'prediction': prediction,
        'data_sources': data_sources,
        'all_predictions': all_predictions,
        'hourly_data': hourly_data
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)