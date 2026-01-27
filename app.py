from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_required, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from weather_service import WeatherService
from models import db, User, SavedCity, OutfitPreference, SavedOutfit, init_system_settings
from auth import init_auth
from utils import track_event, track_affiliate_click, create_response_headers, get_user_preferences
from monitoring import create_monitoring_blueprint, SystemMonitor, AnalyticsReporter
from email_service import get_email_service
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///weather_wiz.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_TIME_LIMIT'] = None

# Security configurations
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
init_auth(app)

# Register blueprints
monitoring_bp = create_monitoring_blueprint()
app.register_blueprint(monitoring_bp)

# Initialize weather service
weather_service = WeatherService()

# Create tables and initialize data
with app.app_context():
    db.create_all()
    init_system_settings()

@app.before_request
def before_request():
    """Add security headers and track page views"""
    # Track page views
    if request.endpoint and not request.endpoint.startswith('static'):
        track_event('page_view', {
            'endpoint': request.endpoint,
            'method': request.method,
            'url': request.url
        })

@app.after_request
def after_request(response):
    """Add security headers to all responses"""
    headers = create_response_headers()
    for key, value in headers.items():
        response.headers[key] = value
    return response

@app.context_processor
def inject_user_data():
    """Inject user data into all templates"""
    if current_user.is_authenticated:
        return {
            'current_city': current_user.default_city,
            'saved_cities': current_user.get_saved_cities_list(),
            'user_preferences': get_user_preferences(current_user)
        }
    return {
        'current_city': session.get('city', 'London'),
        'saved_cities': session.get('saved_cities', []),
        'user_preferences': get_user_preferences(None)
    }

@app.route('/')
def index():
    try:
        # Get city preference
        if current_user.is_authenticated:
            selected_city = current_user.default_city or 'London'
        else:
            selected_city = session.get('city', 'London')
        
        weather_data = weather_service.get_current_weather(selected_city)
        
        if weather_data is None:
            flash('Unable to fetch weather data. Please try again later.', 'error')
            return render_template('index.html', error=True, current_city=selected_city)
            
        # Track weather view
        track_event('weather_viewed', {
            'city': selected_city,
            'temperature': weather_data.get('temperature'),
            'condition': weather_data.get('condition')
        })
            
        return render_template('index.html', weather=weather_data, current_city=selected_city)
        
    except Exception as e:
        logging.error(f"Error in index route: {str(e)}")
        flash('An error occurred while fetching weather data. Please try again later.', 'error')
        return render_template('index.html', error=True, current_city=selected_city if 'selected_city' in locals() else 'London')

@app.route('/forecast')
def forecast():
    """Forecast page showing hourly and daily forecasts"""
    city = request.args.get('city')
    if not city:
        if current_user.is_authenticated:
            city = current_user.default_city or 'London'
        else:
            city = session.get('city', 'London')
    
    try:
        current_weather = weather_service.get_current_weather(city)
        hourly_forecast = weather_service.get_hourly_forecast(city)
        daily_forecast = weather_service.get_daily_forecast(city)
        
        # Track forecast view
        track_event('forecast_viewed', {
            'city': city,
            'type': 'both'
        })
        
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
    if request.method == 'POST':
        city_name = request.form.get('city_name', '').strip()
        action = request.form.get('action')
        
        if action == 'add' and city_name:
            # Verify city exists by trying to get weather
            try:
                weather_data = weather_service.get_current_weather(city_name)
                if weather_data:
                    formatted_city = weather_data['location']
                    
                    if current_user.is_authenticated:
                        # Save to database
                        existing_city = SavedCity.query.filter_by(
                            user_id=current_user.id,
                            city_name=formatted_city
                        ).first()
                        
                        if not existing_city:
                            saved_city = SavedCity(
                                user_id=current_user.id,
                                city_name=formatted_city,
                                country=weather_data.get('location', '').split(', ')[-1] if ', ' in weather_data.get('location', '') else None
                            )
                            db.session.add(saved_city)
                            db.session.commit()
                            
                            track_event('city_saved', {
                                'city': formatted_city,
                                'user_id': current_user.id
                            })
                            
                            flash(f'Added {formatted_city} to your cities', 'success')
                        else:
                            flash(f'{formatted_city} is already in your cities', 'info')
                    else:
                        # Save to session for non-authenticated users
                        saved_cities = session.get('saved_cities', [])
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
            
            if current_user.is_authenticated:
                # Remove from database
                saved_city = SavedCity.query.filter_by(
                    user_id=current_user.id,
                    city_name=city_to_remove
                ).first()
                
                if saved_city:
                    db.session.delete(saved_city)
                    db.session.commit()
                    
                    track_event('city_removed', {
                        'city': city_to_remove,
                        'user_id': current_user.id
                    })
                    
                    flash(f'Removed {city_to_remove} from your cities', 'success')
            else:
                # Remove from session
                saved_cities = session.get('saved_cities', [])
                if city_to_remove in saved_cities:
                    saved_cities.remove(city_to_remove)
                    session['saved_cities'] = saved_cities
                    flash(f'Removed {city_to_remove} from your cities', 'success')
    
    return render_template('search.html')

@app.route('/city/<city>')
def city_weather(city):
    """Individual city weather page - redirects to main page with city parameter"""
    try:
        if current_user.is_authenticated:
            # Update user's default city
            current_user.default_city = city
            db.session.commit()
        else:
            # Save city to session
            session['city'] = city
        
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error in city route: {str(e)}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/map')
def map():
    """Weather map page"""
    if current_user.is_authenticated:
        city = current_user.default_city or 'London'
    else:
        city = session.get('city', 'London')
    
    try:
        # Get coordinates for the city
        current_weather = weather_service.get_current_weather(city)
        if current_weather:
            coordinates = current_weather.get('coordinates', {'lat': 51.5074, 'lon': -0.1278})
        else:
            coordinates = {'lat': 51.5074, 'lon': -0.1278}  # Default to London
        
        track_event('map_viewed', {
            'city': city,
            'coordinates': coordinates
        })
        
        return render_template('map.html', 
                             coordinates=coordinates,
                             current_city=city,
                             api_key=weather_service.api_key)
    except Exception as e:
        logging.error(f"Error loading map for {city}: {str(e)}")
        flash('Unable to load weather map. Please try again.', 'error')
        return render_template('map.html', 
                             coordinates={'lat': 51.5074, 'lon': -0.1278},
                             current_city=city,
                             api_key=weather_service.api_key)

@app.route('/outfit-affiliate')
def outfit_affiliate():
    """Affiliate-based outfit marketplace page"""
    city = request.args.get('city')
    if not city:
        if current_user.is_authenticated:
            city = current_user.default_city or 'London'
        else:
            city = session.get('city', 'London')
    
    try:
        current_weather = weather_service.get_current_weather(city)
        
        # Track outfit marketplace view
        track_event('outfit_marketplace_viewed', {
            'city': city,
            'temperature': current_weather.get('temperature') if current_weather else None,
            'condition': current_weather.get('condition') if current_weather else None
        })
        
        return render_template('outfit_affiliate.html', 
                             current_weather=current_weather,
                             current_city=city)
    except Exception as e:
        logging.error(f"Error loading affiliate outfit page for {city}: {str(e)}")
        flash('Unable to load outfit marketplace. Please try again.', 'error')
        return render_template('outfit_affiliate.html', 
                             current_weather=None,
                             current_city=city)

@app.route('/outfit-preferences')
@login_required
def outfit_preferences():
    """Outfit preferences page"""
    preferences = current_user.outfit_preferences
    if not preferences:
        # Create default preferences
        preferences = OutfitPreference(user_id=current_user.id)
        db.session.add(preferences)
        db.session.commit()
    
    return render_template('outfit_preferences.html', preferences=preferences)

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

@app.route('/api/affiliate-products', methods=['POST'])
def api_affiliate_products():
    """API endpoint for getting affiliate product recommendations"""
    try:
        from affiliate_products import get_products_by_weather
        
        data = request.get_json()
        style = data.get('style', 'casual')
        temperature_category = data.get('temperature_category', 'warm')
        
        # Get products from affiliate database
        products = get_products_by_weather(style, temperature_category)
        
        if not products:
            # Return fallback products if none found
            products = {
                'tops': [{
                    'name': 'Basic T-Shirt',
                    'brand': 'Generic',
                    'price': '$15.99',
                    'affiliateUrl': '#',
                    'image': 'https://via.placeholder.com/300x300?text=T-Shirt',
                    'rating': 4.0,
                    'description': 'Comfortable basic t-shirt',
                    'features': ['Cotton', 'Machine Washable', 'Comfortable Fit']
                }],
                'bottoms': [{
                    'name': 'Basic Pants',
                    'brand': 'Generic',
                    'price': '$29.99',
                    'affiliateUrl': '#',
                    'image': 'https://via.placeholder.com/300x300?text=Pants',
                    'rating': 4.0,
                    'description': 'Comfortable basic pants',
                    'features': ['Cotton Blend', 'Machine Washable', 'Regular Fit']
                }],
                'footwear': [{
                    'name': 'Basic Sneakers',
                    'brand': 'Generic',
                    'price': '$49.99',
                    'affiliateUrl': '#',
                    'image': 'https://via.placeholder.com/300x300?text=Sneakers',
                    'rating': 4.0,
                    'description': 'Comfortable basic sneakers',
                    'features': ['Canvas Upper', 'Rubber Sole', 'Comfortable']
                }],
                'accessories': [{
                    'name': 'Basic Accessory',
                    'brand': 'Generic',
                    'price': '$19.99',
                    'affiliateUrl': '#',
                    'image': 'https://via.placeholder.com/300x300?text=Accessory',
                    'rating': 4.0,
                    'description': 'Basic accessory',
                    'features': ['Durable', 'Stylish', 'Versatile']
                }]
            }
        
        return jsonify(products)
        
    except Exception as e:
        logging.error(f"Error generating affiliate products: {str(e)}")
        return jsonify({'error': 'Unable to generate product recommendations'}), 500

@app.route('/api/track-affiliate-click', methods=['POST'])
def api_track_affiliate_click():
    """API endpoint for tracking affiliate link clicks"""
    try:
        data = request.get_json()
        click_id = track_affiliate_click(data)
        
        return jsonify({
            'success': True,
            'click_id': click_id
        })
        
    except Exception as e:
        logging.error(f"Error tracking affiliate click: {str(e)}")
        return jsonify({'error': 'Unable to track click'}), 500

@app.route('/api/save-outfit', methods=['POST'])
@login_required
def api_save_outfit():
    """API endpoint for saving outfits"""
    try:
        data = request.get_json()
        
        saved_outfit = SavedOutfit(
            user_id=current_user.id,
            outfit_name=data.get('name'),
            style=data.get('style'),
            weather_condition=data.get('weather_condition'),
            temperature=data.get('temperature'),
            city=data.get('city'),
            total_price=data.get('total_price')
        )
        saved_outfit.set_outfit_data(data.get('outfit_data', {}))
        
        db.session.add(saved_outfit)
        db.session.commit()
        
        track_event('outfit_saved', {
            'outfit_id': saved_outfit.id,
            'style': saved_outfit.style,
            'city': saved_outfit.city
        })
        
        return jsonify({
            'success': True,
            'outfit_id': saved_outfit.id
        })
        
    except Exception as e:
        logging.error(f"Error saving outfit: {str(e)}")
        return jsonify({'error': 'Unable to save outfit'}), 500

@app.route('/admin/products')
def admin_products():
    """Admin interface for managing affiliate products"""
    # Add basic authentication here if needed
    return render_template('admin_products.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard with system overview"""
    # Check if user is admin (you can implement proper role checking)
    if not current_user.is_premium:  # Using premium as admin flag for now
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    return render_template('admin_dashboard.html')

@app.route('/api/admin/recent-users')
@login_required
def api_admin_recent_users():
    """API endpoint for getting recent users"""
    if not current_user.is_premium:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
        users_data = [user.to_dict() for user in recent_users]
        
        return jsonify({'users': users_data})
    except Exception as e:
        logging.error(f"Error getting recent users: {e}")
        return jsonify({'error': 'Unable to fetch users'}), 500

@app.route('/api/admin/test-email', methods=['POST'])
@login_required
def api_admin_test_email():
    """Send test email"""
    if not current_user.is_premium:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        success = get_email_service().send_welcome_email(current_user)
        if success:
            return jsonify({'message': 'Test email sent successfully!'})
        else:
            return jsonify({'error': 'Failed to send test email'}), 500
    except Exception as e:
        logging.error(f"Error sending test email: {e}")
        return jsonify({'error': 'Unable to send test email'}), 500

@app.route('/api/admin/clear-cache', methods=['POST'])
@login_required
def api_admin_clear_cache():
    """Clear application cache"""
    if not current_user.is_premium:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        from utils import WeatherCache
        WeatherCache.clear()
        return jsonify({'message': 'Cache cleared successfully!'})
    except Exception as e:
        logging.error(f"Error clearing cache: {e}")
        return jsonify({'error': 'Unable to clear cache'}), 500

@app.route('/api/admin/export-data')
@login_required
def api_admin_export_data():
    """Export system data as CSV"""
    if not current_user.is_premium:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        import csv
        from io import StringIO
        from flask import make_response
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Export user data
        writer.writerow(['Type', 'ID', 'Email', 'Username', 'Created', 'Premium', 'Active'])
        users = User.query.all()
        for user in users:
            writer.writerow([
                'User', user.id, user.email, user.username,
                user.created_at.isoformat() if user.created_at else '',
                user.is_premium, user.is_active
            ])
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=weather-wiz-data-{datetime.now().strftime("%Y%m%d")}.csv'
        
        return response
    except Exception as e:
        logging.error(f"Error exporting data: {e}")
        return jsonify({'error': 'Unable to export data'}), 500

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
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_ENV') != 'production')
