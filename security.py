"""
Security utilities and middleware for Weather Wiz
"""
import os
import hashlib
import secrets
import time
from functools import wraps
from datetime import datetime, timedelta
from flask import request, jsonify, session, current_app, g
from flask_login import current_user
import redis
import logging

# Initialize Redis for rate limiting
redis_client = None
try:
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/1')
    redis_client = redis.from_url(redis_url)
except Exception as e:
    logging.warning(f"Redis not available for rate limiting: {e}")

class SecurityHeaders:
    """Security headers middleware"""
    
    @staticmethod
    def apply_security_headers(response):
        """Apply security headers to response"""
        headers = {
            # Prevent MIME type sniffing
            'X-Content-Type-Options': 'nosniff',
            
            # Prevent clickjacking
            'X-Frame-Options': 'DENY',
            
            # XSS protection
            'X-XSS-Protection': '1; mode=block',
            
            # HTTPS enforcement (only in production)
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains' if not current_app.debug else '',
            
            # Content Security Policy
            'Content-Security-Policy': (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com https://www.googletagmanager.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
                "img-src 'self' data: https: http:; "
                "font-src 'self' https://fonts.gstatic.com; "
                "connect-src 'self' https://api.openweathermap.org https://www.google-analytics.com; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self';"
            ),
            
            # Referrer policy
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            
            # Permissions policy
            'Permissions-Policy': (
                'geolocation=(self), '
                'microphone=(), '
                'camera=(), '
                'payment=(), '
                'usb=(), '
                'magnetometer=(), '
                'gyroscope=(), '
                'speaker=()'
            )
        }
        
        for key, value in headers.items():
            if value:  # Only add non-empty headers
                response.headers[key] = value
        
        return response

class RateLimiter:
    """Rate limiting functionality"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.default_limits = {
            'api': {'requests': 100, 'window': 3600},  # 100 requests per hour
            'auth': {'requests': 5, 'window': 300},    # 5 attempts per 5 minutes
            'search': {'requests': 50, 'window': 3600}, # 50 searches per hour
            'affiliate': {'requests': 200, 'window': 3600}, # 200 affiliate clicks per hour
        }
    
    def get_client_id(self):
        """Get client identifier for rate limiting"""
        if current_user.is_authenticated:
            return f"user:{current_user.id}"
        else:
            return f"ip:{request.remote_addr}"
    
    def is_rate_limited(self, limit_type='api', custom_limit=None):
        """Check if client is rate limited"""
        if not self.redis:
            return False  # No rate limiting if Redis unavailable
        
        try:
            client_id = self.get_client_id()
            limit_config = custom_limit or self.default_limits.get(limit_type, self.default_limits['api'])
            
            key = f"rate_limit:{limit_type}:{client_id}"
            window = limit_config['window']
            max_requests = limit_config['requests']
            
            # Use sliding window rate limiting
            now = time.time()
            pipeline = self.redis.pipeline()
            
            # Remove old entries
            pipeline.zremrangebyscore(key, 0, now - window)
            
            # Count current requests
            pipeline.zcard(key)
            
            # Add current request
            pipeline.zadd(key, {str(now): now})
            
            # Set expiration
            pipeline.expire(key, window)
            
            results = pipeline.execute()
            current_requests = results[1]
            
            return current_requests >= max_requests
            
        except Exception as e:
            logging.error(f"Rate limiting error: {e}")
            return False  # Fail open
    
    def get_rate_limit_info(self, limit_type='api'):
        """Get rate limit information for client"""
        if not self.redis:
            return None
        
        try:
            client_id = self.get_client_id()
            limit_config = self.default_limits.get(limit_type, self.default_limits['api'])
            
            key = f"rate_limit:{limit_type}:{client_id}"
            window = limit_config['window']
            max_requests = limit_config['requests']
            
            now = time.time()
            
            # Clean old entries and count current
            self.redis.zremrangebyscore(key, 0, now - window)
            current_requests = self.redis.zcard(key)
            
            # Get oldest request time for reset calculation
            oldest = self.redis.zrange(key, 0, 0, withscores=True)
            reset_time = int(oldest[0][1] + window) if oldest else int(now + window)
            
            return {
                'limit': max_requests,
                'remaining': max(0, max_requests - current_requests),
                'reset': reset_time,
                'window': window
            }
            
        except Exception as e:
            logging.error(f"Rate limit info error: {e}")
            return None

# Global rate limiter instance
rate_limiter = RateLimiter(redis_client)

def rate_limit(limit_type='api', custom_limit=None):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if rate_limiter.is_rate_limited(limit_type, custom_limit):
                rate_info = rate_limiter.get_rate_limit_info(limit_type)
                
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Try again later.',
                    'rate_limit': rate_info
                })
                response.status_code = 429
                
                if rate_info:
                    response.headers['X-RateLimit-Limit'] = str(rate_info['limit'])
                    response.headers['X-RateLimit-Remaining'] = str(rate_info['remaining'])
                    response.headers['X-RateLimit-Reset'] = str(rate_info['reset'])
                
                return response
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class InputValidator:
    """Input validation and sanitization"""
    
    @staticmethod
    def sanitize_string(text, max_length=None, allow_html=False):
        """Sanitize string input"""
        if not text:
            return ''
        
        # Convert to string and strip whitespace
        text = str(text).strip()
        
        # Remove HTML tags if not allowed
        if not allow_html:
            import re
            text = re.sub(r'<[^>]+>', '', text)
        
        # Truncate if needed
        if max_length and len(text) > max_length:
            text = text[:max_length].strip()
        
        return text
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password_strength(password):
        """Validate password strength"""
        import re
        
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
    
    @staticmethod
    def validate_city_name(city_name):
        """Validate city name input"""
        if not city_name:
            return False
        
        # Basic validation - letters, spaces, hyphens, apostrophes
        import re
        pattern = r"^[a-zA-Z\s\-'\.]+$"
        return re.match(pattern, city_name) and len(city_name) <= 100

class SessionSecurity:
    """Session security utilities"""
    
    @staticmethod
    def generate_csrf_token():
        """Generate CSRF token"""
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_hex(16)
        return session['csrf_token']
    
    @staticmethod
    def validate_csrf_token(token):
        """Validate CSRF token"""
        return token and session.get('csrf_token') == token
    
    @staticmethod
    def regenerate_session():
        """Regenerate session ID for security"""
        # Store important data
        user_id = session.get('_user_id')
        csrf_token = session.get('csrf_token')
        
        # Clear session
        session.clear()
        
        # Restore important data
        if user_id:
            session['_user_id'] = user_id
        if csrf_token:
            session['csrf_token'] = csrf_token
    
    @staticmethod
    def check_session_security():
        """Check session security and detect anomalies"""
        current_ip = request.remote_addr
        current_ua = request.headers.get('User-Agent', '')
        
        # Check for IP changes (optional - can be disabled for mobile users)
        if 'session_ip' in session:
            if session['session_ip'] != current_ip:
                logging.warning(f"Session IP changed: {session['session_ip']} -> {current_ip}")
                # Optionally invalidate session or require re-authentication
        else:
            session['session_ip'] = current_ip
        
        # Check for user agent changes
        if 'session_ua' in session:
            if session['session_ua'] != current_ua:
                logging.warning(f"Session User-Agent changed")
                # Optionally invalidate session
        else:
            session['session_ua'] = current_ua
        
        # Update last activity
        session['last_activity'] = datetime.utcnow().isoformat()

def require_https(f):
    """Decorator to require HTTPS in production"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.debug and not request.is_secure:
            return redirect(request.url.replace('http://', 'https://'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Check if user is admin (using premium flag for now)
        if not current_user.is_premium:
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def log_security_event(event_type, details=None):
    """Log security-related events"""
    try:
        from models import UserAnalytics
        
        event_data = {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', ''),
            'endpoint': request.endpoint,
            'method': request.method,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if details:
            event_data.update(details)
        
        # Log to database
        analytics = UserAnalytics(
            user_id=current_user.id if current_user.is_authenticated else None,
            event_type=f'security_{event_type}',
            session_id=session.get('session_id'),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        analytics.set_event_data(event_data)
        
        from models import db
        db.session.add(analytics)
        db.session.commit()
        
        # Also log to file
        logging.warning(f"Security event - {event_type}: {event_data}")
        
    except Exception as e:
        logging.error(f"Failed to log security event: {e}")

def init_security(app):
    """Initialize security features for Flask app"""
    
    @app.before_request
    def security_before_request():
        """Security checks before each request"""
        # Check session security
        SessionSecurity.check_session_security()
        
        # Add rate limit headers
        if hasattr(g, 'rate_limit_info'):
            pass  # Headers will be added by rate limit decorator
    
    @app.after_request
    def security_after_request(response):
        """Apply security headers after each request"""
        return SecurityHeaders.apply_security_headers(response)
    
    # Register security context processors
    @app.context_processor
    def security_context():
        return {
            'csrf_token': SessionSecurity.generate_csrf_token()
        }