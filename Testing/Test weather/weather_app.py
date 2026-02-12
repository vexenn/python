import requests
import json
from datetime import datetime

class NOAAWeatherApp:
    def __init__(self):
        self.base_url = 'https://api.weather.gov'
        self.headers = {
            'User-Agent': 'MyPythonWeather/1.0 (vexenn897@gmail.com)'
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
            'Detroit': (42.3314, -83.0458)
        }
    
    def get_point_data(self, latitude, longitude):
        """Get metadata for a specific lat/lon point"""
        url = f'{self.base_url}/points/{latitude},{longitude}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting point {response.status_code}')
            return None
    
    def get_forecast(self, latitude, longitude):
        """Get 12-hour forecast periods"""
        point_data = self.get_point_data(latitude, longitude)
        
        if point_data:
            forecast_url = point_data['properties']['forecast']
            response = requests.get(forecast_url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Error getting forecast: {response.status_code}')
                return None
        return None
    
    def get_hourly_forecast(self, latitude, longitude):
        """Get hourly forecast"""
        point_data = self.get_point_data(latitude, longitude)
        
        if point_data:
            forecast_url = point_data['properties']['forecastHourly']
            response = requests.get(forecast_url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Error getting hourly forecast: {response.status_code}')
                return None
        return None
    
    def get_current_observations(self, station_id):
        """Get latest weather observations from a station"""
        url = f'{self.base_url}/stations/{station_id}/observations/latest'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting observations: {response.status_code}')
            return None
    
    def get_nearby_stations(self, latitude, longitude):
        """Get nearby weather stations"""
        point_data = self.get_point_data(latitude, longitude)
        
        if point_data:
            stations_url = point_data['properties']['observationStations']
            response = requests.get(stations_url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Error getting stations: {response.status_code}')
                return None
        return None
    
    def get_alerts_by_point(self, latitude, longitude):
        """Get active alerts for a specific location"""
        url = f'{self.base_url}/alerts/active?point={latitude},{longitude}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting alerts by point: {response.status_code}')
            return None
    
    def get_city_coordinates(self, city_name):
        """Get coordinates for a city"""
        city_name = city_name.strip().title()
        
        if city_name in self.cities:
            return self.cities[city_name]
        else:
            print(f"City '{city_name}' not found in database.")
            print(f"Available cities: {', '.join(sorted(set(self.cities.keys())))}")
            return None
    
    def get_highest_temp_today(self, city_name):
        """Get highest temperature forecast for today"""
        coords = self.get_city_coordinates(city_name)
        if not coords:
            return None
        
        lat, lon = coords
        forecast = self.get_forecast(lat, lon)
        
        if forecast:
            periods = forecast['properties']['periods']
            today_periods = [p for p in periods if 'Today' in p['name'] or 'This Afternoon' in p['name']]
            
            if today_periods:
                temp = today_periods[0]['temperature']
                return temp
            elif periods:
                return periods[0]['temperature']
        
        return None
    
    def get_lowest_temp_today(self, city_name):
        """Get lowest temperature forecast for today"""
        coords = self.get_city_coordinates(city_name)
        if not coords:
            return None
        
        lat, lon = coords
        forecast = self.get_forecast(lat, lon)
        
        if forecast:
            periods = forecast['properties']['periods']
            tonight_periods = [p for p in periods if 'Tonight' in p['name'] or 'Night' in p['name']]
            
            if tonight_periods:
                temp = tonight_periods[0]['temperature']
                return temp
        
        return None
    
    def will_it_rain_today(self, city_name):
        """Check if it will rain today"""
        coords = self.get_city_coordinates(city_name)
        if not coords:
            return None
        
        lat, lon = coords
        forecast = self.get_hourly_forecast(lat, lon)
        
        if forecast:
            periods = forecast['properties']['periods'][:24]  # Next 24 hours
            
            for period in periods:
                short_forecast = period.get('shortForecast', '').lower()
                if 'rain' in short_forecast or 'shower' in short_forecast or 'storm' in short_forecast:
                    return "Yes"
            
            return "No"
        
        return None
    
    def get_current_temp(self, city_name):
        """Get current temperature"""
        coords = self.get_city_coordinates(city_name)
        if not coords:
            return None
        
        lat, lon = coords
        stations_data = self.get_nearby_stations(lat, lon)
        
        if stations_data and stations_data.get('features'):
            station_id = stations_data['features'][0]['properties']['stationIdentifier']
            obs = self.get_current_observations(station_id)
            
            if obs:
                temp = obs['properties'].get('temperature', {})
                if temp and temp.get('value') is not None:
                    temp_f = temp['value'] * 9/5 + 32 if 'degC' in temp.get('unitCode', '') else temp['value']
                    return round(temp_f)
        
        return None


def interactive_weather_query():
    """Interactive weather query system"""
    weather = NOAAWeatherApp()
    
    print("\n" + "="*60)
    print("🌤️  WEATHER PREDICTION MARKETS - INTERACTIVE QUERY")
    print("="*60)
    
    while True:
        print("\n" + "-"*60)
        print("QUERY OPTIONS:")
        print("-"*60)
        print("1. Highest temperature in [CITY] today?")
        print("2. Lowest temperature in [CITY] today?")
        print("3. Will it rain in [CITY] today?")
        print("4. Current temperature in [CITY]?")
        print("5. Compare temperatures across multiple cities")
        print("6. Show available cities")
        print("7. Exit")
        print("-"*60)
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            city = input("Enter city name: ").strip()
            temp = weather.get_highest_temp_today(city)
            if temp:
                print(f"\n📊 Highest temperature in {city} today?")
                print(f"   🌡️  {temp}°F")
                print(f"   Range: {temp-1}° to {temp+1}°F")
        
        elif choice == '2':
            city = input("Enter city name: ").strip()
            temp = weather.get_lowest_temp_today(city)
            if temp:
                print(f"\n📊 Lowest temperature in {city} today?")
                print(f"   🌡️  {temp}°F")
                print(f"   Range: {temp-1}° to {temp+1}°F")
        
        elif choice == '3':
            city = input("Enter city name: ").strip()
            rain = weather.will_it_rain_today(city)
            if rain:
                print(f"\n📊 Will it rain in {city} today?")
                print(f"   💧 {rain}")
        
        elif choice == '4':
            city = input("Enter city name: ").strip()
            temp = weather.get_current_temp(city)
            if temp:
                print(f"\n📊 Current temperature in {city}?")
                print(f"   🌡️  {temp}°F")
        
        elif choice == '5':
            cities_input = input("Enter cities separated by commas (e.g., NYC, LA, Miami): ").strip()
            cities = [c.strip() for c in cities_input.split(',')]
            
            print(f"\n📊 Temperature Comparison:")
            print("-"*60)
            
            for city in cities:
                temp = weather.get_highest_temp_today(city)
                if temp:
                    print(f"   {city:20} → {temp}°F (range: {temp-1}° to {temp+1}°)")
        
        elif choice == '6':
            print(f"\n📍 Available Cities:")
            print("-"*60)
            cities_list = sorted(set(weather.cities.keys()))
            for i, city in enumerate(cities_list, 1):
                print(f"{i:2}. {city}")
        
        elif choice == '7':
            print("\n👋 Thank you for using Weather Prediction Markets!")
            break
        
        else:
            print("\n❌ Invalid option. Please try again.")


def quick_climate_dashboard():
    """Quick dashboard showing multiple cities"""
    weather = NOAAWeatherApp()
    
    major_cities = ['NYC', 'LA', 'Miami', 'Austin', 'Chicago', 
                    'Washington DC', 'Denver', 'Philadelphia', 'San Francisco', 'Phoenix']
    
    print("\n" + "="*70)
    print("🌍  CLIMATE DASHBOARD - TODAY'S TEMPERATURE FORECAST")
    print("="*70)
    print(f"{'CITY':<20} {'HIGHEST TEMP':<15} {'PREDICTED RANGE':<20}")
    print("-"*70)
    
    for city in major_cities:
        temp = weather.get_highest_temp_today(city)
        if temp:
            range_str = f"{temp-1}° to {temp+1}°F"
            print(f"{city:<20} {temp}°F{'':<10} {range_str:<20}")
        else:
            print(f"{city:<20} {'N/A':<15} {'N/A':<20}")
    
    print("="*70)


# Main menu
def main():
    print("\n" + "="*60)
    print("🌤️  NOAA WEATHER APP")
    print("="*60)
    print("\nSelect Mode:")
    print("1. Interactive Query Mode")
    print("2. Quick Climate Dashboard")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        interactive_weather_query()
    elif choice == '2':
        quick_climate_dashboard()
    elif choice == '3':
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice")


if __name__ == "__main__":
    main()