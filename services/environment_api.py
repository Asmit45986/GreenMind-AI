import requests
import json

class EnvironmentDataFetcher:
    def __init__(self, api_key="YOUR_OPENWEATHER_API_KEY"):
        self.api_key = api_key
        self.weather_url = "http://api.openweathermap.org/data/2.5/weather"
        self.aqi_url = "http://api.openweathermap.org/data/2.5/air_pollution"

    def fetch_weather(self, lat, lon):
        params = {'lat': lat, 'lon': lon, 'appid': self.api_key, 'units': 'metric'}
        try:
            response = requests.get(self.weather_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "data": {
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'rainfall_1h': data.get('rain', {}).get('1h', 0.0),
                        'weather_main': data['weather'][0]['main'],
                        'location_name': data.get('name', 'Unknown Location')
                    }
                }
            else:
                return {"status": "error", "message": f"Weather API Failed: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fetch_aqi(self, lat, lon):
        params = {'lat': lat, 'lon': lon, 'appid': self.api_key}
        try:
            response = requests.get(self.aqi_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                aqi_val = data['list'][0]['main']['aqi']
                components = data['list'][0]['components']
                return {
                    "status": "success",
                    "data": {
                        'aqi_index': aqi_val,
                        'pm2_5': components.get('pm2_5', 0.0),
                        'pm10': components.get('pm10', 0.0),
                        'co': components.get('co', 0.0)
                    }
                }
            else:
                return {"status": "error", "message": f"AQI API Failed: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_full_environmental_profile(self, lat, lon):
        print(f"🌐 Fetching environmental profile for Lat: {lat}, Lon: {lon}...")
        
        weather_res = self.fetch_weather(lat, lon)
        aqi_res = self.fetch_aqi(lat, lon)
        
        # 💡 FALLBACK MECHANISM: Agar API fail hoti hai (jaise 401 error), toh mock profile return karega taaki pipeline na ruke!
        if weather_res['status'] == 'error' or aqi_res['status'] == 'error':
            print("⚠️ API Authentication/Activation Pending. Serving simulated fallback environmental data...")
            mock_profile = {
                'location': 'Simulated Region (Fallback)',
                'coordinates': {'latitude': lat, 'longitude': lon},
                'weather': {
                    'temperature': 32.5,  # Standard tropical temperature
                    'humidity': 45.0,     # Moderate humidity
                    'wind_speed': 3.4,
                    'rainfall_1h': 0.0,
                    'weather_main': 'Clear'
                },
                'air_quality': {
                    'aqi_index': 3,       # Moderate AQI
                    'pm2_5': 35.0,
                    'pm10': 70.0,
                    'co': 400.0
                }
            }
            return {"status": "success_fallback", "profile": mock_profile}
            
        return {
            "status": "success",
            "profile": {
                'location': weather_res['data']['location_name'],
                'coordinates': {'latitude': lat, 'longitude': lon},
                'weather': weather_res['data'],
                'air_quality': aqi_res['data']
            }
        }