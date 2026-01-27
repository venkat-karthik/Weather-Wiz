"""
Configuration settings for Weather Wiz application
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///weather_wiz.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Security configuration
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Email configuration
    MAIL_SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('SMTP_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('SMTP_USERNAME')
    MAIL_PASSWORD = os.environ.get('SMTP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('FROM_EMAIL') or os.environ.get('SMTP_USERNAME')
    
    # Redis configuration (for caching and sessions)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Celery configuration (for background tasks)
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 16 * 1024 * 1024)  # 16MB
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    
    # API configuration
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    AMAZON_AFFILIATE_TAG = os.environ.get('AMAZON_AFFILIATE_TAG') or 'your-affiliate-tag-20'
    
    # Monitoring and analytics
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID')
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/1'
    
    # Application settings
    ITEMS_PER_PAGE = 20
    MAX_SAVED_CITIES = 10
    MAX_SAVED_OUTFITS = 50
    
    # Feature flags
    ENABLE_REGISTRATION = os.environ.get('ENABLE_REGISTRATION', 'true').lower() == 'true'
    ENABLE_EMAIL_VERIFICATION = os.environ.get('ENABLE_EMAIL_VERIFICATION', 'false').lower() == 'true'
    ENABLE_ANALYTICS = os.environ.get('ENABLE_ANALYTICS', 'true').lower() == 'true'
    ENABLE_AFFILIATE_TRACKING = os.environ.get('ENABLE_AFFILIATE_TRACKING', 'true').lower() == 'true'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Less strict security for development
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = True
    
    # Development database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///weather_wiz_dev.db'
    
    # Development email (use console backend)
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Disable email sending in tests
    MAIL_SUPPRESS_SEND = True
    
    # Disable analytics in tests
    ENABLE_ANALYTICS = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Strict security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Production database (PostgreSQL recommended)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:pass@localhost/weather_wiz'
    
    # Production logging
    LOG_LEVEL = 'INFO'
    
    # Security headers
    FORCE_HTTPS = True
    
    # Performance optimizations
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True,
        'max_overflow': 20
    }

class DockerConfig(ProductionConfig):
    """Docker container configuration"""
    
    # Docker-specific database URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://weather_user:weather_pass@db:5432/weather_wiz'
    
    # Docker Redis URL
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://redis:6379/0'
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or 'redis://redis:6379/0'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])