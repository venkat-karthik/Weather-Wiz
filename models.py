"""
Database models for Weather Wiz application
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    
    # User preferences
    default_city = db.Column(db.String(100), default='London')
    temperature_unit = db.Column(db.String(10), default='celsius')  # celsius, fahrenheit
    theme_preference = db.Column(db.String(10), default='auto')  # light, dark, auto
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_premium = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    saved_cities = db.relationship('SavedCity', backref='user', lazy=True, cascade='all, delete-orphan')
    outfit_preferences = db.relationship('OutfitPreference', backref='user', uselist=False, cascade='all, delete-orphan')
    saved_outfits = db.relationship('SavedOutfit', backref='user', lazy=True, cascade='all, delete-orphan')
    analytics = db.relationship('UserAnalytics', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_saved_cities_list(self):
        """Get list of saved city names"""
        return [city.city_name for city in self.saved_cities]
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'default_city': self.default_city,
            'temperature_unit': self.temperature_unit,
            'theme_preference': self.theme_preference,
            'is_premium': self.is_premium,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SavedCity(db.Model):
    """Model for user's saved cities"""
    __tablename__ = 'saved_cities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'city_name', name='unique_user_city'),)

class OutfitPreference(db.Model):
    """Model for user's outfit preferences"""
    __tablename__ = 'outfit_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Style preferences
    preferred_style = db.Column(db.String(20), default='casual')  # casual, formal, sporty, trendy
    comfort_level = db.Column(db.String(20), default='medium')  # low, medium, high
    budget_range = db.Column(db.String(20), default='medium')  # low, medium, high
    
    # Color preferences (JSON array)
    preferred_colors = db.Column(db.Text, default='["blue", "black", "white", "gray"]')
    
    # Other preferences
    include_accessories = db.Column(db.Boolean, default=True)
    layering_preference = db.Column(db.String(20), default='medium')  # light, medium, heavy
    footwear_preference = db.Column(db.String(20), default='comfortable')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_preferred_colors(self):
        """Get preferred colors as list"""
        try:
            return json.loads(self.preferred_colors)
        except:
            return ["blue", "black", "white", "gray"]
    
    def set_preferred_colors(self, colors):
        """Set preferred colors from list"""
        self.preferred_colors = json.dumps(colors)

class SavedOutfit(db.Model):
    """Model for user's saved outfits"""
    __tablename__ = 'saved_outfits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Outfit details
    outfit_name = db.Column(db.String(100), nullable=True)
    style = db.Column(db.String(20), nullable=False)
    weather_condition = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    
    # Outfit items (JSON)
    outfit_data = db.Column(db.Text, nullable=False)  # JSON with product details
    total_price = db.Column(db.Float, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_outfit_data(self):
        """Get outfit data as dictionary"""
        try:
            return json.loads(self.outfit_data)
        except:
            return {}
    
    def set_outfit_data(self, data):
        """Set outfit data from dictionary"""
        self.outfit_data = json.dumps(data)

class UserAnalytics(db.Model):
    """Model for tracking user analytics and behavior"""
    __tablename__ = 'user_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for anonymous users
    
    # Event tracking
    event_type = db.Column(db.String(50), nullable=False)  # page_view, outfit_view, affiliate_click, etc.
    event_data = db.Column(db.Text, nullable=True)  # JSON with additional event data
    
    # Session info
    session_id = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    
    # Location and context
    city = db.Column(db.String(100), nullable=True)
    weather_condition = db.Column(db.String(50), nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_event_data(self):
        """Get event data as dictionary"""
        try:
            return json.loads(self.event_data) if self.event_data else {}
        except:
            return {}
    
    def set_event_data(self, data):
        """Set event data from dictionary"""
        self.event_data = json.dumps(data) if data else None

class AffiliateClick(db.Model):
    """Model for tracking affiliate link clicks and conversions"""
    __tablename__ = 'affiliate_clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Product info
    product_name = db.Column(db.String(200), nullable=False)
    product_brand = db.Column(db.String(100), nullable=True)
    product_price = db.Column(db.Float, nullable=True)
    amazon_asin = db.Column(db.String(20), nullable=True)
    affiliate_url = db.Column(db.Text, nullable=False)
    
    # Context
    weather_condition = db.Column(db.String(50), nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    outfit_style = db.Column(db.String(20), nullable=True)
    
    # Tracking
    session_id = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    referrer = db.Column(db.Text, nullable=True)
    
    # Conversion tracking (to be updated via Amazon API or manual tracking)
    converted = db.Column(db.Boolean, default=False)
    conversion_value = db.Column(db.Float, nullable=True)
    conversion_date = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemSettings(db.Model):
    """Model for system-wide settings and configuration"""
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_setting(key, default=None):
        """Get a system setting value"""
        setting = SystemSettings.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set_setting(key, value, description=None):
        """Set a system setting value"""
        setting = SystemSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            if description:
                setting.description = description
        else:
            setting = SystemSettings(key=key, value=value, description=description)
            db.session.add(setting)
        db.session.commit()
        return setting

# Initialize default system settings
def init_system_settings():
    """Initialize default system settings"""
    default_settings = [
        ('affiliate_tag', 'your-affiliate-tag-20', 'Amazon affiliate tag'),
        ('site_name', 'Weather Wiz', 'Site name'),
        ('site_description', 'Weather-based outfit recommendations with affiliate shopping', 'Site description'),
        ('maintenance_mode', 'false', 'Maintenance mode flag'),
        ('analytics_enabled', 'true', 'Analytics tracking enabled'),
        ('email_notifications', 'true', 'Email notifications enabled'),
        ('max_saved_cities', '10', 'Maximum saved cities per user'),
        ('max_saved_outfits', '50', 'Maximum saved outfits per user'),
    ]
    
    for key, value, description in default_settings:
        if not SystemSettings.query.filter_by(key=key).first():
            setting = SystemSettings(key=key, value=value, description=description)
            db.session.add(setting)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing system settings: {e}")