"""
Vercel-optimized version of Weather Wiz application
"""
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import json

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Basic configuration for Vercel
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "vercel-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_wiz_vercel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize weather service
try:
    from weather_service import WeatherService
    weather_service = WeatherService()
except ImportError:
    weather_service = None
    logging.warning("Weather service not available")

@app.route('/')
def index():
    """Main page with weather display"""
    try:
        # Get city preference from session
        selected_city = session.get('city', 'London')
        
        if weather_service:
            weather_data = weather_service.get_current_weather(selected_city)
        else:
            # Fallback weather data for demo
            weather_data = {
                'location': selected_city,
                'temperature': 20,
                'condition': 'Clear',
                'description': 'Clear sky',
                'humidity': 65,
                'wind_speed': 5.2,
                'icon': '01d'
            }
        
        if weather_data is None:
            flash('Unable to fetch weather data. Please try again later.', 'error')
            return render_template('index.html', error=True, current_city=selected_city)
            
        return render_template('index.html', weather=weather_data, current_city=selected_city)
        
    except Exception as e:
        logging.error(f"Error in index route: {str(e)}")
        flash('An error occurred while fetching weather data. Please try again later.', 'error')
        return render_template('index.html', error=True, current_city='London')

@app.route('/forecast')
def forecast():
    """Forecast page showing hourly and daily forecasts"""
    city = request.args.get('city', 'London')
    
    try:
        if weather_service:
            current_weather = weather_service.get_current_weather(city)
            hourly_forecast = weather_service.get_hourly_forecast(city)
            daily_forecast = weather_service.get_daily_forecast(city)
        else:
            # Fallback data
            current_weather = {'location': city, 'temperature': 20, 'condition': 'Clear'}
            hourly_forecast = []
            daily_forecast = []
        
        return render_template('forecast.html', 
                             current_weather=current_weather,
                             hourly_forecast=hourly_forecast,
                             daily_forecast=daily_forecast,
                             current_city=city)
    except Exception as e:
        logging.error(f"Error fetching forecast for {city}: {str(e)}")
        flash('Unable to fetch forecast data. Please try again.', 'error')
        return render_template('forecast.html', 
                             current_weather=None,
                             hourly_forecast=[],
                             daily_forecast=[],
                             current_city=city)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search for cities and manage saved cities"""
    saved_cities = session.get('saved_cities', [])
    current_city = session.get('city', 'London')
    
    if request.method == 'POST':
        city_name = request.form.get('city_name', '').strip()
        action = request.form.get('action')
        
        if action == 'add' and city_name:
            try:
                if weather_service:
                    weather_data = weather_service.get_current_weather(city_name)
                    if weather_data:
                        formatted_city = weather_data['location']
                        if formatted_city not in saved_cities:
                            saved_cities.append(formatted_city)
                            session['saved_cities'] = saved_cities
                            flash(f'Added {formatted_city} to your cities', 'success')
                        else:
                            flash(f'{formatted_city} is already in your cities', 'info')
                    else:
                        flash(f'City "{city_name}" not found', 'error')
                else:
                    # Fallback - just add the city
                    if city_name not in saved_cities:
                        saved_cities.append(city_name)
                        session['saved_cities'] = saved_cities
                        flash(f'Added {city_name} to your cities', 'success')
            except Exception as e:
                logging.error(f"Error adding city {city_name}: {str(e)}")
                flash('Unable to add city. Please try again.', 'error')
        
        elif action == 'remove':
            city_to_remove = request.form.get('city_to_remove')
            if city_to_remove in saved_cities:
                saved_cities.remove(city_to_remove)
                session['saved_cities'] = saved_cities
                flash(f'Removed {city_to_remove} from your cities', 'success')
    
    return render_template('search.html', saved_cities=saved_cities, current_city=current_city)

@app.route('/city/<city>')
def city_weather(city):
    """Individual city weather page - redirects to main page with city parameter"""
    try:
        session['city'] = city
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error in city route: {str(e)}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/map')
def map():
    """Weather map page"""
    city = session.get('city', 'London')
    saved_cities = session.get('saved_cities', [])
    
    try:
        if weather_service:
            current_weather = weather_service.get_current_weather(city)
            if current_weather:
                coordinates = current_weather.get('coordinates', {'lat': 51.5074, 'lon': -0.1278})
            else:
                coordinates = {'lat': 51.5074, 'lon': -0.1278}
        else:
            coordinates = {'lat': 51.5074, 'lon': -0.1278}
        
        api_key = os.environ.get('OPENWEATHER_API_KEY', '')
        
        return render_template('map.html', 
                             coordinates=coordinates,
                             saved_cities=saved_cities,
                             current_city=city,
                             api_key=api_key)
    except Exception as e:
        logging.error(f"Error loading map for {city}: {str(e)}")
        flash('Unable to load weather map. Please try again.', 'error')
        return render_template('map.html', 
                             coordinates={'lat': 51.5074, 'lon': -0.1278},
                             saved_cities=saved_cities,
                             current_city=city,
                             api_key='')

@app.route('/outfit-affiliate')
def outfit_affiliate():
    """Affiliate-based outfit marketplace page"""
    city = request.args.get('city', 'London')
    saved_cities = session.get('saved_cities', [])
    
    try:
        if weather_service:
            current_weather = weather_service.get_current_weather(city)
        else:
            current_weather = {'location': city, 'temperature': 20, 'condition': 'Clear'}
            
        return render_template('outfit_affiliate.html', 
                             current_weather=current_weather,
                             saved_cities=saved_cities,
                             current_city=city)
    except Exception as e:
        logging.error(f"Error loading affiliate outfit page for {city}: {str(e)}")
        flash('Unable to load outfit marketplace. Please try again.', 'error')
        return render_template('outfit_affiliate.html', 
                             current_weather=None,
                             saved_cities=saved_cities,
                             current_city=city)

@app.route('/api/weather/<city>')
def api_weather(city):
    """API endpoint for getting weather data"""
    try:
        if weather_service:
            weather_data = weather_service.get_current_weather(city)
            if weather_data:
                return jsonify(weather_data)
        
        # Fallback response
        return jsonify({
            'location': city,
            'temperature': 20,
            'condition': 'Clear',
            'description': 'Weather data unavailable'
        })
    except Exception as e:
        logging.error(f"API error for {city}: {str(e)}")
        return jsonify({'error': 'Weather service unavailable'}), 500

@app.route('/api/affiliate-products', methods=['POST'])
def api_affiliate_products():
    """API endpoint for getting affiliate product recommendations"""
    try:
        data = request.get_json() or {}
        style = data.get('style', 'casual')
        temperature_category = data.get('temperature_category', 'warm')
        
        try:
            import affiliate_products
            products = affiliate_products.get_products_by_weather(style, temperature_category)
        except Exception as err:
            logging.error(f"Failed to load affiliate products module: {str(err)}")
            products = {}
            
        # Default structure fallback
        if not products:
            products = {'tops': [], 'bottoms': [], 'footwear': [], 'accessories': []}
            
        return jsonify(products)
        
    except Exception as e:
        logging.error(f"Error generating affiliate products: {str(e)}")
        return jsonify({'error': 'Unable to generate product recommendations'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'environment': 'vercel'
    })

@app.route('/privacy')
def privacy_policy():
    """Privacy policy page"""
    return render_template('legal/privacy.html')

@app.route('/terms')
def terms_of_service():
    """Terms of service page"""
    return render_template('legal/terms.html')

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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

# For Vercel deployment
if __name__ == '__main__':
    app.run(debug=False)