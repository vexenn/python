import sys
import os
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta
import statistics
import traceback

# Get the base path (works for both development and PyInstaller)
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = sys._MEIPASS
else:
    # Running in normal Python environment
    base_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(base_path, 'templates'))

class NOAAWeatherApp:
    def __init__(self):
        self.base_url = 'https://api.weather.gov'
        self.headers = {
            'User-Agent': 'WeatherPrediction/2.0 (weather@example.com)'
        }
        
        # Popular US Cities with coordinates
        self.cities = {
            'New York': (40.7128, -74.0060),
            'NYC': (40.7128, -74.0060),
            'Los Angeles': (34.0522, -118.2437),
            'LA': (34.0522, -118.2437),
            'Chicago': (41.8781, -87.6298),
            'Houston': (29.7604, -95.3698),
            'Phoenix': (33.4484, -112.0740),
            'Philadelphia': (39.9526, -75.1652),
            'San Antonio': (29.4241, -98.4936),
            'San Diego': (32.7157, -117.1611),
            'Dallas': (32.7767, -96.7970),
            'Miami': (25.7617, -80.1918),
            'Seattle': (47.6062, -122.3321),
            'Denver': (39.7392, -104.9903),
            'Boston': (42.3601, -71.0589),
            'Atlanta': (33.7490, -84.3880),
            'Las Vegas': (36.1699, -115.1398),
            'Washington DC': (38.9072, -77.0369),
            'DC': (38.9072, -77.0369),
            'San Francisco': (37.7749, -122.4194),
            'Minneapolis': (44.9778, -93.2650),
            'Austin': (30.2672, -97.7431),
            'New Orleans': (29.9511, -90.0715),
            'Oklahoma City': (35.4676, -97.5164),
            'Salt Lake City': (40.7608, -111.8910),
            'Detroit': (42.3314, -83.0458),
            'Portland': (45.5152, -122.6784),
            'Memphis': (35.1495, -90.0490),
            'Nashville': (36.1627, -86.7816),
            'Baltimore': (39.2904, -76.6122)
        }
    
    def get_point_data(self, latitude, longitude):
        """Get metadata for a specific lat/lon point"""
        url = f'{self.base_url}/points/{latitude},{longitude}'
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f'Error getting point {e}')
        return None
    
    def get_forecast(self, latitude, longitude):
        """Get 12-hour forecast periods"""
        point_data = self.get_point_data(latitude, longitude)
        
        if point_data:
            try:
                forecast_url = point_data['properties']['forecast']
                response = requests.get(forecast_url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f'Error getting forecast: {e}')
        return None
    
    def get_hourly_forecast(self, latitude, longitude):
        """Get hourly forecast"""
        point_data = self.get_point_data(latitude, longitude)
        
        if point_data:
            try:
                forecast_url = point_data['properties']['forecastHourly']
                response = requests.get(forecast_url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f'Error getting hourly forecast: {e}')
        return None
    
    def get_nearby_stations(self, latitude, longitude):
        """Get nearby weather stations"""
        point_data = self.get_point_data(latitude, longitude)
        
        if point_data:
            try:
                stations_url = point_data['properties']['observationStations']
                response = requests.get(stations_url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f'Error getting stations: {e}')
        return None
    
    def get_current_observations(self, station_id):
        """Get latest weather observations from a station"""
        url = f'{self.base_url}/stations/{station_id}/observations/latest'
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f'Error getting observations: {e}')
        return None
    
    def get_city_coordinates(self, city_name):
        """Get coordinates for a city"""
        city_name = city_name.strip().title()
        
        if city_name.upper() in ['NYC', 'LA', 'DC']:
            city_name = city_name.upper()
        
        if city_name in self.cities:
            return self.cities[city_name]
        
        # Try partial match
        for key in self.cities.keys():
            if city_name.lower() in key.lower():
                return self.cities[key]
        
        return None
    
    def calculate_advanced_prediction(self, city_name):
        """Advanced prediction algorithm using multiple data sources"""
        coords = self.get_city_coordinates(city_name)
        if not coords:
            return None
        
        lat, lon = coords
        
        # Collect all temperature data points
        temp_predictions = []
        data_sources = []
        
        # 1. Get standard forecast
        try:
            forecast = self.get_forecast(lat, lon)
            if forecast and 'properties' in forecast:
                periods = forecast['properties']['periods']
                for period in periods[:3]:
                    if 'today' in period['name'].lower() or 'this afternoon' in period['name'].lower():
                        temp_predictions.append(period['temperature'])
                        data_sources.append(f"Standard Forecast - {period['name']}")
        except Exception as e:
            print(f"Error processing forecast: {e}")
        
        # 2. Get hourly forecast for more granular data
        hourly_temps = []
        hourly_data = []
        try:
            hourly = self.get_hourly_forecast(lat, lon)
            if hourly and 'properties' in hourly:
                now = datetime.now()
                periods = hourly['properties']['periods']
                
                for period in periods[:24]:
                    try:
                        period_time = datetime.fromisoformat(period['startTime'].replace('Z', '+00:00'))
                        if period_time.date() == now.date():
                            hourly_temps.append(period['temperature'])
                            hourly_data.append({
                                'temp': period['temperature'],
                                'time': period_time.strftime('%I:%M %p'),
                                'hour': period_time.strftime('%I %p').lstrip('0')
                            })
                    except:
                        continue
                
                if hourly_temps:
                    hourly_max = max(hourly_temps)
                    temp_predictions.append(hourly_max)
                    data_sources.append(f"Hourly Max ({len(hourly_temps)} hours)")
        except Exception as e:
            print(f"Error processing hourly: {e}")
        
        # 3. Get current observation
        current_temp = None
        try:
            stations_data = self.get_nearby_stations(lat, lon)
            
            if stations_data and stations_data.get('features'):
                station_id = stations_data['features'][0]['properties']['stationIdentifier']
                obs = self.get_current_observations(station_id)
                
                if obs and 'properties' in obs:
                    temp = obs['properties'].get('temperature', {})
                    if temp and temp.get('value') is not None:
                        temp_c = temp['value']
                        current_temp = round(temp_c * 9/5 + 32)
        except Exception as e:
            print(f"Error getting current temp: {e}")
        
        if not temp_predictions:
            return None
        
        # Calculate statistics
        predicted_high = round(statistics.median(temp_predictions))
        mean_temp = round(statistics.mean(temp_predictions))
        
        if len(temp_predictions) > 1:
            std_dev = statistics.stdev(temp_predictions)
            confidence = max(0, min(100, 100 - (std_dev * 10)))
        else:
            confidence = 70
        
        if confidence >= 90:
            range_offset = 1
        elif confidence >= 75:
            range_offset = 2
        else:
            range_offset = 3
        
        result = {
            'city': city_name,
            'predicted_high': predicted_high,
            'prediction_range_low': predicted_high - range_offset,
            'prediction_range_high': predicted_high + range_offset,
            'confidence_score': round(confidence, 1),
            'current_temp': current_temp,
            'data_points_used': len(temp_predictions),
            'data_sources': data_sources,
            'all_predictions': temp_predictions,
            'mean_prediction': mean_temp,
            'hourly_temps': hourly_temps if hourly_temps else None,
            'hourly_data': hourly_data if hourly_data else None,
            'analysis': self._generate_analysis(temp_predictions, predicted_high, confidence, current_temp)
        }
        
        return result
    
    def _generate_analysis(self, predictions, predicted_high, confidence, current_temp):
        """Generate human-readable analysis"""
        analysis = []
        
        if len(predictions) >= 3:
            analysis.append(f"✅ High confidence - {len(predictions)} data sources agree")
        elif len(predictions) == 2:
            analysis.append(f"⚠️ Moderate confidence - {len(predictions)} data sources available")
        else:
            analysis.append(f"⚠️ Limited data - only {len(predictions)} source available")
        
        if confidence >= 90:
            analysis.append("📊 Very high accuracy expected (90%+ confidence)")
        elif confidence >= 75:
            analysis.append("📊 High accuracy expected (75%+ confidence)")
        else:
            analysis.append("📊 Moderate accuracy expected")
        
        if current_temp:
            temp_diff = predicted_high - current_temp
            if temp_diff > 10:
                analysis.append(f"🌡️ Temperature expected to rise {temp_diff}°F from current")
            elif temp_diff < -5:
                analysis.append(f"🌡️ Temperature expected to drop {abs(temp_diff)}°F from current")
            else:
                analysis.append("🌡️ Temperature relatively stable")
        
        variance = max(predictions) - min(predictions)
        if variance <= 3:
            analysis.append("✨ All forecasts closely aligned (±3°F)")
        elif variance <= 5:
            analysis.append("📉 Forecasts show minor variation (±5°F)")
        else:
            analysis.append("⚠️ Forecasts show some disagreement")
        
        return analysis


# Initialize weather app
weather_app = NOAAWeatherApp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get list of available cities"""
    cities = sorted(set(weather_app.cities.keys()))
    return jsonify({'cities': cities})

@app.route('/api/prediction/<city>', methods=['GET'])
def get_prediction(city):
    """Get advanced temperature prediction for a city"""
    try:
        prediction = weather_app.calculate_advanced_prediction(city)
        
        if prediction:
            return jsonify(prediction)
        else:
            return jsonify({'error': 'City not found or data unavailable'}), 404
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare-predictions', methods=['POST'])
def compare_predictions():
    """Compare predictions across multiple cities"""
    try:
        cities = request.json.get('cities', [])
        
        results = []
        for city in cities:
            prediction = weather_app.calculate_advanced_prediction(city)
            if prediction:
                results.append(prediction)
        
        return jsonify({'results': results})
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def open_browser():
    """Open browser after a short delay"""
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Auto-open browser
    Timer(1, open_browser).start()
    
    print("=" * 50)
    print("🌡️  Weather Prediction System Starting...")
    print("=" * 50)
    print("📍 Server running at: http://127.0.0.1:5000")
    print("🌐 Browser will open automatically...")
    print("⚠️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(debug=False, port=5000, use_reloader=False)