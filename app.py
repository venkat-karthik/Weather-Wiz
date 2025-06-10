import os
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from weather_service import WeatherService
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_weather_secret_key")

# Initialize weather service
weather_service = WeatherService()

@app.route('/')
def index():
    """Home page showing current weather"""
    # Get default city or first saved city
    saved_cities = session.get('saved_cities', [])
    current_city = request.args.get('city') or (saved_cities[0] if saved_cities else 'London')
    
    try:
        current_weather = weather_service.get_current_weather(current_city)
        if current_weather:
            return render_template('index.html', 
                                 weather=current_weather, 
                                 saved_cities=saved_cities,
                                 current_city=current_city)
        else:
            flash('Unable to fetch weather data. Please try again.', 'error')
            return render_template('index.html', 
                                 weather=None, 
                                 saved_cities=saved_cities,
                                 current_city=current_city)
    except Exception as e:
        logging.error(f"Error fetching weather for {current_city}: {str(e)}")
        flash('Weather service is currently unavailable. Please try again later.', 'error')
        return render_template('index.html', 
                             weather=None, 
                             saved_cities=saved_cities,
                             current_city=current_city)

@app.route('/forecast')
def forecast():
    """Forecast page showing hourly and daily forecasts"""
    city = request.args.get('city', 'London')
    saved_cities = session.get('saved_cities', [])
    
    try:
        current_weather = weather_service.get_current_weather(city)
        hourly_forecast = weather_service.get_hourly_forecast(city)
        daily_forecast = weather_service.get_daily_forecast(city)
        
        return render_template('forecast.html', 
                             current_weather=current_weather,
                             hourly_forecast=hourly_forecast,
                             daily_forecast=daily_forecast,
                             saved_cities=saved_cities,
                             current_city=city)
    except Exception as e:
        logging.error(f"Error fetching forecast for {city}: {str(e)}")
        flash('Unable to fetch forecast data. Please try again.', 'error')
        return render_template('forecast.html', 
                             current_weather=None,
                             hourly_forecast=[],
                             daily_forecast=[],
                             saved_cities=saved_cities,
                             current_city=city)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search for cities and manage saved cities"""
    saved_cities = session.get('saved_cities', [])
    
    if request.method == 'POST':
        city_name = request.form.get('city_name', '').strip()
        action = request.form.get('action')
        
        if action == 'add' and city_name:
            # Verify city exists by trying to get weather
            try:
                weather_data = weather_service.get_current_weather(city_name)
                if weather_data:
                    # Get the properly formatted city name from the API response
                    formatted_city = weather_data['location']
                    if formatted_city not in saved_cities:
                        saved_cities.append(formatted_city)
                        session['saved_cities'] = saved_cities
                        flash(f'Added {formatted_city} to your cities', 'success')
                    else:
                        flash(f'{formatted_city} is already in your cities', 'info')
                else:
                    flash(f'City "{city_name}" not found', 'error')
            except Exception as e:
                logging.error(f"Error adding city {city_name}: {str(e)}")
                flash('Unable to add city. Please try again.', 'error')
        
        elif action == 'remove':
            city_to_remove = request.form.get('city_to_remove')
            if city_to_remove in saved_cities:
                saved_cities.remove(city_to_remove)
                session['saved_cities'] = saved_cities
                flash(f'Removed {city_to_remove} from your cities', 'success')
    
    return render_template('search.html', saved_cities=saved_cities)

@app.route('/city/<city_name>')
def city_weather(city_name):
    """Individual city weather page"""
    saved_cities = session.get('saved_cities', [])
    
    try:
        current_weather = weather_service.get_current_weather(city_name)
        hourly_forecast = weather_service.get_hourly_forecast(city_name)[:8]  # Next 8 hours
        
        if current_weather:
            return render_template('city.html', 
                                 weather=current_weather,
                                 hourly_forecast=hourly_forecast,
                                 saved_cities=saved_cities,
                                 current_city=city_name)
        else:
            flash(f'Weather data for {city_name} not available', 'error')
            return redirect(url_for('search'))
    except Exception as e:
        logging.error(f"Error fetching weather for city {city_name}: {str(e)}")
        flash('Unable to fetch weather data. Please try again.', 'error')
        return redirect(url_for('search'))

@app.route('/map')
def weather_map():
    """Weather map page"""
    city = request.args.get('city', 'London')
    saved_cities = session.get('saved_cities', [])
    
    try:
        # Get coordinates for the city
        current_weather = weather_service.get_current_weather(city)
        if current_weather:
            coordinates = current_weather.get('coordinates', {'lat': 51.5074, 'lon': -0.1278})
        else:
            coordinates = {'lat': 51.5074, 'lon': -0.1278}  # Default to London
        
        return render_template('map.html', 
                             coordinates=coordinates,
                             saved_cities=saved_cities,
                             current_city=city,
                             api_key=weather_service.api_key)
    except Exception as e:
        logging.error(f"Error loading map for {city}: {str(e)}")
        flash('Unable to load weather map. Please try again.', 'error')
        return render_template('map.html', 
                             coordinates={'lat': 51.5074, 'lon': -0.1278},
                             saved_cities=saved_cities,
                             current_city=city,
                             api_key=weather_service.api_key)

@app.route('/api/weather/<city>')
def api_weather(city):
    """API endpoint for getting weather data (for AJAX updates)"""
    try:
        weather_data = weather_service.get_current_weather(city)
        if weather_data:
            return jsonify(weather_data)
        else:
            return jsonify({'error': 'Weather data not available'}), 404
    except Exception as e:
        logging.error(f"API error for {city}: {str(e)}")
        return jsonify({'error': 'Weather service unavailable'}), 500

@app.route('/api/weather-by-coords')
def api_weather_by_coords():
    """API endpoint for getting weather data by coordinates"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if not lat or not lon:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        # Use reverse geocoding to get city name, then get weather
        import requests
        geocoding_url = f"https://api.openweathermap.org/geo/1.0/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'limit': 1,
            'appid': weather_service.api_key
        }
        
        response = requests.get(geocoding_url, params=params, timeout=10)
        response.raise_for_status()
        location_data = response.json()
        
        if location_data:
            city_name = location_data[0]['name']
            return redirect(url_for('index', city=city_name))
        else:
            return jsonify({'error': 'Location not found'}), 404
            
    except Exception as e:
        logging.error(f"Coordinates API error: {str(e)}")
        return jsonify({'error': 'Unable to get location weather'}), 500

@app.template_filter('timestamp_to_time')
def timestamp_to_time(timestamp):
    """Convert timestamp to readable time"""
    try:
        return datetime.fromtimestamp(timestamp).strftime('%H:%M')
    except:
        return 'N/A'

@app.template_filter('timestamp_to_day')
def timestamp_to_day(timestamp):
    """Convert timestamp to day name"""
    try:
        return datetime.fromtimestamp(timestamp).strftime('%A')
    except:
        return 'N/A'

@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    """Convert timestamp to readable date"""
    try:
        return datetime.fromtimestamp(timestamp).strftime('%b %d')
    except:
        return 'N/A'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
