"""
Utility functions for Weather Wiz application
"""
import re
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request, session
from models import db, UserAnalytics, AffiliateClick
from datetime import datetime
import hashlib
import secrets
import json

def validate_email(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_session_id():
    """Generate a unique session ID"""
    return hashlib.sha256(secrets.token_bytes(32)).hexdigest()

def get_client_ip():
    """Get client IP address"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def get_user_agent():
    """Get user agent string"""
    return request.headers.get('User-Agent', '')

def track_event(event_type, event_data=None, user_id=None):
    """Track user events for analytics"""
    try:
        from flask_login import current_user
        
        # Get user ID
        if user_id is None and hasattr(current_user, 'id'):
            user_id = current_user.id if current_user.is_authenticated else None
        
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = generate_session_id()
        
        # Create analytics record
        analytics = UserAnalytics(
            user_id=user_id,
            event_type=event_type,
            session_id=session['session_id'],
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )
        
        if event_data:
            analytics.set_event_data(event_data)
        
        db.session.add(analytics)
        db.session.commit()
        
    except Exception as e:
        logging.error(f"Error tracking event {event_type}: {str(e)}")
        db.session.rollback()

def track_affiliate_click(product_data, user_id=None):
    """Track affiliate link clicks"""
    try:
        from flask_login import current_user
        
        if user_id is None and hasattr(current_user, 'id'):
            user_id = current_user.id if current_user.is_authenticated else None
        
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = generate_session_id()
        
        click = AffiliateClick(
            user_id=user_id,
            product_name=product_data.get('name', ''),
            product_brand=product_data.get('brand', ''),
            product_price=float(product_data.get('price', '0').replace('$', '')) if product_data.get('price') else None,
            amazon_asin=product_data.get('amazon_asin', ''),
            affiliate_url=product_data.get('affiliateUrl', ''),
            weather_condition=product_data.get('weather_condition'),
            temperature=product_data.get('temperature'),
            city=product_data.get('city'),
            outfit_style=product_data.get('style'),
            session_id=session['session_id'],
            ip_address=get_client_ip(),
            referrer=request.referrer
        )
        
        db.session.add(click)
        db.session.commit()
        
        return click.id
        
    except Exception as e:
        logging.error(f"Error tracking affiliate click: {str(e)}")
        db.session.rollback()
        return None

def send_email(to_email, subject, body, html_body=None):
    """Send email using SMTP"""
    try:
        smtp_server = os.environ.get('SMTP_SERVER')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SMTP_USERNAME')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        from_email = os.environ.get('FROM_EMAIL', smtp_username)
        
        if not all([smtp_server, smtp_username, smtp_password]):
            logging.error("Email configuration missing")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Add text part
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return False

def format_currency(amount, currency='USD'):
    """Format currency amount"""
    if currency == 'USD':
        return f"${amount:.2f}"
    elif currency == 'EUR':
        return f"€{amount:.2f}"
    elif currency == 'GBP':
        return f"£{amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"

def sanitize_input(text, max_length=None):
    """Sanitize user input"""
    if not text:
        return ''
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length].strip()
    
    return text

def generate_slug(text):
    """Generate URL-friendly slug from text"""
    # Convert to lowercase
    slug = text.lower()
    
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    
    return slug

def calculate_temperature_category(temp_celsius):
    """Calculate temperature category for outfit recommendations"""
    if temp_celsius >= 25:
        return 'hot'
    elif temp_celsius >= 18:
        return 'warm'
    elif temp_celsius >= 10:
        return 'mild'
    elif temp_celsius >= 5:
        return 'cool'
    elif temp_celsius >= 0:
        return 'cold'
    else:
        return 'freezing'

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9

def get_weather_icon_url(icon_code, size='2x'):
    """Get OpenWeatherMap icon URL"""
    return f"https://openweathermap.org/img/wn/{icon_code}@{size}.png"

def is_mobile_device():
    """Check if request is from mobile device"""
    user_agent = request.headers.get('User-Agent', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'tablet', 'phone']
    return any(keyword in user_agent for keyword in mobile_keywords)

def get_country_from_ip(ip_address):
    """Get country from IP address (requires GeoIP service)"""
    # This would integrate with a GeoIP service like MaxMind
    # For now, return None
    return None

def log_error(error, context=None):
    """Log error with context"""
    error_msg = f"Error: {str(error)}"
    if context:
        error_msg += f" | Context: {json.dumps(context)}"
    
    logging.error(error_msg)

def create_response_headers():
    """Create security headers for responses"""
    return {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https: http:; font-src 'self' https://fonts.gstatic.com; connect-src 'self' https://api.openweathermap.org;"
    }

def rate_limit_key(identifier):
    """Generate rate limit key"""
    return f"rate_limit:{identifier}:{datetime.now().strftime('%Y-%m-%d-%H-%M')}"

def validate_password_strength(password):
    """Validate password strength"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return errors

def generate_api_key():
    """Generate API key for external integrations"""
    return secrets.token_urlsafe(32)

def hash_api_key(api_key):
    """Hash API key for storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()

def verify_api_key(api_key, hashed_key):
    """Verify API key against hash"""
    return hashlib.sha256(api_key.encode()).hexdigest() == hashed_key

class WeatherCache:
    """Simple in-memory cache for weather data"""
    _cache = {}
    _cache_timeout = 600  # 10 minutes
    
    @classmethod
    def get(cls, key):
        """Get cached data"""
        if key in cls._cache:
            data, timestamp = cls._cache[key]
            if datetime.now().timestamp() - timestamp < cls._cache_timeout:
                return data
            else:
                del cls._cache[key]
        return None
    
    @classmethod
    def set(cls, key, data):
        """Set cached data"""
        cls._cache[key] = (data, datetime.now().timestamp())
    
    @classmethod
    def clear(cls):
        """Clear all cached data"""
        cls._cache.clear()

def get_user_preferences(user):
    """Get user preferences with defaults"""
    if not user or not user.is_authenticated:
        return {
            'temperature_unit': 'celsius',
            'theme_preference': 'auto',
            'default_city': 'London'
        }
    
    return {
        'temperature_unit': user.temperature_unit or 'celsius',
        'theme_preference': user.theme_preference or 'auto',
        'default_city': user.default_city or 'London'
    }