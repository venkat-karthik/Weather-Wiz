"""
Authentication and user management for Weather Wiz
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, SavedCity, OutfitPreference, UserAnalytics
from utils import track_event, validate_email, send_email
import re
from datetime import datetime

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email', '').strip().lower()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        # Validation
        errors = []
        
        if not email or not validate_email(email):
            errors.append('Please enter a valid email address.')
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Username can only contain letters, numbers, and underscores.')
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            errors.append('An account with this email already exists.')
        
        if User.query.filter_by(username=username).first():
            errors.append('This username is already taken.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        try:
            # Create new user
            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Create default outfit preferences
            outfit_prefs = OutfitPreference(user_id=user.id)
            db.session.add(outfit_prefs)
            
            # Add default city (London)
            default_city = SavedCity(
                user_id=user.id,
                city_name='London',
                country='UK',
                is_default=True
            )
            db.session.add(default_city)
            
            db.session.commit()
            
            # Track registration
            track_event('user_registered', {
                'user_id': user.id,
                'email': email,
                'username': username
            })
            
            # Log in the user
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash('Registration successful! Welcome to Weather Wiz!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email_or_username = request.form.get('email_or_username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') == 'on'
        
        if not email_or_username or not password:
            flash('Please enter both email/username and password.', 'error')
            return render_template('auth/login.html')
        
        # Find user by email or username
        user = None
        if '@' in email_or_username:
            user = User.query.filter_by(email=email_or_username.lower()).first()
        else:
            user = User.query.filter_by(username=email_or_username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'error')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember_me)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Track login
            track_event('user_login', {
                'user_id': user.id,
                'email': user.email
            })
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            
            flash(f'Welcome back, {user.first_name or user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email/username or password.', 'error')
            track_event('login_failed', {
                'email_or_username': email_or_username
            })
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    track_event('user_logout', {
        'user_id': current_user.id
    })
    
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        default_city = request.form.get('default_city', '').strip()
        temperature_unit = request.form.get('temperature_unit', 'celsius')
        theme_preference = request.form.get('theme_preference', 'auto')
        
        # Validation
        if temperature_unit not in ['celsius', 'fahrenheit']:
            temperature_unit = 'celsius'
        
        if theme_preference not in ['light', 'dark', 'auto']:
            theme_preference = 'auto'
        
        try:
            # Update user
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.default_city = default_city or 'London'
            current_user.temperature_unit = temperature_unit
            current_user.theme_preference = theme_preference
            current_user.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            track_event('profile_updated', {
                'user_id': current_user.id
            })
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'error')
    
    return render_template('auth/edit_profile.html', user=current_user)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 8:
            flash('New password must be at least 8 characters long.', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('auth/change_password.html')
        
        try:
            current_user.set_password(new_password)
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            
            track_event('password_changed', {
                'user_id': current_user.id
            })
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while changing your password.', 'error')
    
    return render_template('auth/change_password.html')

@auth_bp.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    """Delete user account"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_delete = request.form.get('confirm_delete') == 'on'
        
        if not current_user.check_password(password):
            flash('Password is incorrect.', 'error')
            return render_template('auth/delete_account.html')
        
        if not confirm_delete:
            flash('Please confirm that you want to delete your account.', 'error')
            return render_template('auth/delete_account.html')
        
        try:
            user_id = current_user.id
            email = current_user.email
            
            # Track account deletion
            track_event('account_deleted', {
                'user_id': user_id,
                'email': email
            })
            
            # Delete user (cascade will handle related records)
            db.session.delete(current_user)
            db.session.commit()
            
            # Log out user
            logout_user()
            
            flash('Your account has been deleted successfully.', 'info')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting your account.', 'error')
    
    return render_template('auth/delete_account.html')

@auth_bp.route('/api/check-username')
def check_username():
    """API endpoint to check if username is available"""
    username = request.args.get('username', '').strip()
    
    if not username or len(username) < 3:
        return jsonify({'available': False, 'message': 'Username must be at least 3 characters long.'})
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({'available': False, 'message': 'Username can only contain letters, numbers, and underscores.'})
    
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'available': False, 'message': 'This username is already taken.'})
    
    return jsonify({'available': True, 'message': 'Username is available.'})

@auth_bp.route('/api/check-email')
def check_email():
    """API endpoint to check if email is available"""
    email = request.args.get('email', '').strip().lower()
    
    if not email or not validate_email(email):
        return jsonify({'available': False, 'message': 'Please enter a valid email address.'})
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'available': False, 'message': 'An account with this email already exists.'})
    
    return jsonify({'available': True, 'message': 'Email is available.'})

# Password reset functionality (requires email setup)
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password - send reset email"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email or not validate_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate reset token (implement token generation)
            # Send reset email (implement email sending)
            track_event('password_reset_requested', {
                'user_id': user.id,
                'email': email
            })
        
        # Always show success message for security
        flash('If an account with that email exists, we have sent a password reset link.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

def init_auth(app):
    """Initialize authentication with Flask app"""
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)