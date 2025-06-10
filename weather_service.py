import os
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class WeatherService:
    """Service class for interacting with OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENWEATHER_API_KEY', 'your_api_key_here')
        self.base_url = 'https://api.openweathermap.org/data/2.5'
        self.geocoding_url = 'https://api.openweathermap.org/geo/1.0'
        
    def get_current_weather(self, city: str) -> Optional[Dict]:
        """Get current weather for a city"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Parse and format the weather data
            weather_data = {
                'location': f"{data['name']}, {data['sys']['country']}",
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'].title(),
                'condition': data['weather'][0]['main'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'uv_index': 0,  # Will be fetched separately
                'sunrise': data['sys']['sunrise'],
                'sunset': data['sys']['sunset'],
                'coordinates': {
                    'lat': data['coord']['lat'],
                    'lon': data['coord']['lon']
                },
                'last_updated': datetime.now().strftime('%H:%M')
            }
            
            # Get UV index
            uv_data = self.get_uv_index(data['coord']['lat'], data['coord']['lon'])
            if uv_data:
                weather_data['uv_index'] = round(uv_data.get('value', 0), 1)
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for {city}: {str(e)}")
            return None
        except KeyError as e:
            logging.error(f"Unexpected API response format for {city}: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Error getting weather for {city}: {str(e)}")
            return None
    
    def get_hourly_forecast(self, city: str) -> List[Dict]:
        """Get hourly forecast for a city (next 24 hours)"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            hourly_data = []
            for item in data['list'][:8]:  # Next 8 periods (24 hours)
                forecast_item = {
                    'time': item['dt'],
                    'temperature': round(item['main']['temp']),
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                    'precipitation': item.get('pop', 0) * 100,  # Convert to percentage
                    'wind_speed': item['wind']['speed']
                }
                hourly_data.append(forecast_item)
            
            return hourly_data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for hourly forecast {city}: {str(e)}")
            return []
        except Exception as e:
            logging.error(f"Error getting hourly forecast for {city}: {str(e)}")
            return []
    
    def get_daily_forecast(self, city: str) -> List[Dict]:
        """Get daily forecast for a city (next 7 days)"""
        try:
            # First get coordinates
            current_weather = self.get_current_weather(city)
            if not current_weather:
                return []
            
            coords = current_weather['coordinates']
            url = f"{self.base_url}/onecall"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric',
                'exclude': 'minutely,alerts'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            daily_data = []
            for item in data['daily'][:7]:  # Next 7 days
                forecast_item = {
                    'date': item['dt'],
                    'temp_max': round(item['temp']['max']),
                    'temp_min': round(item['temp']['min']),
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                    'precipitation': item.get('pop', 0) * 100,  # Convert to percentage
                    'humidity': item['humidity'],
                    'wind_speed': item['wind_speed']
                }
                daily_data.append(forecast_item)
            
            return daily_data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for daily forecast {city}: {str(e)}")
            return []
        except Exception as e:
            logging.error(f"Error getting daily forecast for {city}: {str(e)}")
            return []
    
    def get_uv_index(self, lat: float, lon: float) -> Optional[Dict]:
        """Get UV index for coordinates"""
        try:
            url = f"{self.base_url}/uvi"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for UV index: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Error getting UV index: {str(e)}")
            return None
    
    def get_air_quality(self, lat: float, lon: float) -> Optional[Dict]:
        """Get air quality data for coordinates"""
        try:
            url = f"{self.base_url}/air_pollution"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('list'):
                aqi_data = data['list'][0]
                return {
                    'aqi': aqi_data['main']['aqi'],
                    'co': aqi_data['components']['co'],
                    'no2': aqi_data['components']['no2'],
                    'o3': aqi_data['components']['o3'],
                    'pm2_5': aqi_data['components']['pm2_5'],
                    'pm10': aqi_data['components']['pm10']
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for air quality: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Error getting air quality: {str(e)}")
            return None
    
    def search_cities(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for cities by name"""
        try:
            url = f"{self.geocoding_url}/direct"
            params = {
                'q': query,
                'limit': limit,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            cities = []
            for item in data:
                city_info = {
                    'name': item['name'],
                    'country': item['country'],
                    'state': item.get('state', ''),
                    'lat': item['lat'],
                    'lon': item['lon'],
                    'display_name': f"{item['name']}, {item['country']}"
                }
                if city_info['state']:
                    city_info['display_name'] = f"{item['name']}, {item['state']}, {item['country']}"
                
                cities.append(city_info)
            
            return cities
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for city search {query}: {str(e)}")
            return []
        except Exception as e:
            logging.error(f"Error searching cities for {query}: {str(e)}")
            return []
