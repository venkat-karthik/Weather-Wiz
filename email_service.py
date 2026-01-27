"""
Email Service for Weather Wiz
Handles all email communications including notifications, alerts, and marketing
"""
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from jinja2 import Template
from models import User, SystemSettings
from utils import track_event

class EmailService:
    """Email service for sending various types of emails"""
    
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_username = os.environ.get('SMTP_USERNAME')
        self.smtp_password = os.environ.get('SMTP_PASSWORD')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_username)
        self.site_name = SystemSettings.get_setting('site_name', 'Weather Wiz')
        
    def _create_connection(self):
        """Create SMTP connection"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            return server
        except Exception as e:
            logging.error(f"Failed to create SMTP connection: {e}")
            return None
    
    def _send_email(self, to_email, subject, html_body, text_body=None, attachments=None):
        """Send email with HTML and optional text body"""
        try:
            if not all([self.smtp_server, self.smtp_username, self.smtp_password]):
                logging.error("Email configuration incomplete")
                return False
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.site_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text part if provided
            if text_body:
                text_part = MIMEText(text_body, 'plain')
                msg.attach(text_part)
            
            # Add HTML part
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    with open(attachment['path'], 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {attachment["filename"]}'
                        )
                        msg.attach(part)
            
            # Send email
            server = self._create_connection()
            if not server:
                return False
            
            server.send_message(msg)
            server.quit()
            
            # Track email sent
            track_event('email_sent', {
                'to_email': to_email,
                'subject': subject,
                'type': 'system'
            })
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_welcome_email(self, user):
        """Send welcome email to new users"""
        try:
            template = Template("""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Welcome to {{ site_name }}</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                    .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                    .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                    .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to {{ site_name }}! 🌤️</h1>
                    </div>
                    <div class="content">
                        <h2>Hi {{ user_name }},</h2>
                        <p>Welcome to Weather Wiz! We're excited to have you join our community of weather-conscious fashion enthusiasts.</p>
                        
                        <h3>What you can do with Weather Wiz:</h3>
                        <ul>
                            <li>🌡️ Get accurate weather forecasts for your location</li>
                            <li>👔 Discover weather-appropriate outfit recommendations</li>
                            <li>🛍️ Shop curated fashion items through our affiliate marketplace</li>
                            <li>📱 Save your favorite cities and outfit preferences</li>
                            <li>🎯 Get personalized suggestions based on your style</li>
                        </ul>
                        
                        <p>Ready to get started?</p>
                        <a href="{{ base_url }}" class="button">Explore Weather Wiz</a>
                        
                        <p>If you have any questions, feel free to reach out to our support team.</p>
                        
                        <p>Best regards,<br>The Weather Wiz Team</p>
                    </div>
                    <div class="footer">
                        <p>© {{ current_year }} {{ site_name }}. All rights reserved.</p>
                        <p>You received this email because you signed up for {{ site_name }}.</p>
                    </div>
                </div>
            </body>
            </html>
            """)
            
            html_body = template.render(
                site_name=self.site_name,
                user_name=user.first_name or user.username,
                base_url=os.environ.get('BASE_URL', 'http://localhost:5000'),
                current_year=datetime.now().year
            )
            
            subject = f"Welcome to {self.site_name}! 🌤️"
            
            return self._send_email(user.email, subject, html_body)
            
        except Exception as e:
            logging.error(f"Failed to send welcome email to {user.email}: {e}")
            return False
    
    def send_password_reset_email(self, user, reset_token):
        """Send password reset email"""
        try:
            template = Template("""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Password Reset - {{ site_name }}</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: #dc3545; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                    .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                    .button { display: inline-block; background: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                    .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }
                    .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Reset Request</h1>
                    </div>
                    <div class="content">
                        <h2>Hi {{ user_name }},</h2>
                        <p>We received a request to reset your password for your {{ site_name }} account.</p>
                        
                        <p>Click the button below to reset your password:</p>
                        <a href="{{ reset_url }}" class="button">Reset Password</a>
                        
                        <div class="warning">
                            <strong>Security Notice:</strong>
                            <ul>
                                <li>This link will expire in 1 hour</li>
                                <li>If you didn't request this reset, please ignore this email</li>
                                <li>Never share this link with anyone</li>
                            </ul>
                        </div>
                        
                        <p>If the button doesn't work, copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #666;">{{ reset_url }}</p>
                        
                        <p>Best regards,<br>The {{ site_name }} Team</p>
                    </div>
                    <div class="footer">
                        <p>© {{ current_year }} {{ site_name }}. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """)
            
            reset_url = f"{os.environ.get('BASE_URL', 'http://localhost:5000')}/auth/reset-password/{reset_token}"
            
            html_body = template.render(
                site_name=self.site_name,
                user_name=user.first_name or user.username,
                reset_url=reset_url,
                current_year=datetime.now().year
            )
            
            subject = f"Password Reset - {self.site_name}"
            
            return self._send_email(user.email, subject, html_body)
            
        except Exception as e:
            logging.error(f"Failed to send password reset email to {user.email}: {e}")
            return False
    
    def send_system_alert_email(self, alert_data, admin_emails):
        """Send system alert email to administrators"""
        try:
            template = Template("""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>System Alert - {{ site_name }}</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: #dc3545; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                    .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                    .alert { background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 10px 0; }
                    .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 10px 0; }
                    .info { background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 10px 0; }
                    .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🚨 System Alert</h1>
                    </div>
                    <div class="content">
                        <h2>System Alert Notification</h2>
                        <p><strong>Time:</strong> {{ timestamp }}</p>
                        
                        <h3>Alerts:</h3>
                        {% for alert in alerts %}
                        <div class="{% if alert.level == 'critical' %}alert{% elif alert.level == 'warning' %}warning{% else %}info{% endif %}">
                            <strong>{{ alert.type|title }} ({{ alert.level|title }}):</strong><br>
                            {{ alert.message }}
                        </div>
                        {% endfor %}
                        
                        <h3>System Status:</h3>
                        {% if system_stats %}
                        <ul>
                            <li><strong>CPU Usage:</strong> {{ system_stats.cpu.percent }}%</li>
                            <li><strong>Memory Usage:</strong> {{ system_stats.memory.percent }}%</li>
                            <li><strong>Disk Usage:</strong> {{ system_stats.disk.percent }}%</li>
                        </ul>
                        {% endif %}
                        
                        <p>Please investigate and take appropriate action if necessary.</p>
                        
                        <p>Best regards,<br>{{ site_name }} Monitoring System</p>
                    </div>
                    <div class="footer">
                        <p>© {{ current_year }} {{ site_name }}. All rights reserved.</p>
                        <p>This is an automated system alert.</p>
                    </div>
                </div>
            </body>
            </html>
            """)
            
            html_body = template.render(
                site_name=self.site_name,
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
                alerts=alert_data.get('alerts', []),
                system_stats=alert_data.get('system_stats'),
                current_year=datetime.now().year
            )
            
            subject = f"🚨 System Alert - {self.site_name}"
            
            # Send to all admin emails
            success_count = 0
            for email in admin_emails:
                if self._send_email(email, subject, html_body):
                    success_count += 1
            
            return success_count > 0
            
        except Exception as e:
            logging.error(f"Failed to send system alert email: {e}")
            return False
    
    def send_weekly_report_email(self, user, report_data):
        """Send weekly analytics report to premium users"""
        try:
            template = Template("""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Weekly Report - {{ site_name }}</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                    .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                    .stat-box { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    .stat-number { font-size: 2em; font-weight: bold; color: #667eea; }
                    .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Your Weekly Weather Wiz Report 📊</h1>
                    </div>
                    <div class="content">
                        <h2>Hi {{ user_name }},</h2>
                        <p>Here's your personalized weekly report for {{ week_period }}:</p>
                        
                        <div class="stat-box">
                            <div class="stat-number">{{ weather_checks }}</div>
                            <p>Weather checks this week</p>
                        </div>
                        
                        <div class="stat-box">
                            <div class="stat-number">{{ outfit_views }}</div>
                            <p>Outfit recommendations viewed</p>
                        </div>
                        
                        <div class="stat-box">
                            <div class="stat-number">{{ cities_visited }}</div>
                            <p>Different cities explored</p>
                        </div>
                        
                        {% if favorite_weather %}
                        <h3>Your Weather Patterns:</h3>
                        <p>Most checked weather condition: <strong>{{ favorite_weather }}</strong></p>
                        {% endif %}
                        
                        {% if top_city %}
                        <p>Most visited city: <strong>{{ top_city }}</strong></p>
                        {% endif %}
                        
                        <h3>This Week's Weather Highlights:</h3>
                        <ul>
                            <li>Highest temperature: {{ max_temp }}°C</li>
                            <li>Lowest temperature: {{ min_temp }}°C</li>
                            <li>Most common condition: {{ common_condition }}</li>
                        </ul>
                        
                        <p>Keep exploring and stay weather-ready!</p>
                        
                        <p>Best regards,<br>The {{ site_name }} Team</p>
                    </div>
                    <div class="footer">
                        <p>© {{ current_year }} {{ site_name }}. All rights reserved.</p>
                        <p>You're receiving this as a premium member. <a href="{{ unsubscribe_url }}">Unsubscribe</a></p>
                    </div>
                </div>
            </body>
            </html>
            """)
            
            html_body = template.render(
                site_name=self.site_name,
                user_name=user.first_name or user.username,
                week_period=report_data.get('week_period', 'this week'),
                weather_checks=report_data.get('weather_checks', 0),
                outfit_views=report_data.get('outfit_views', 0),
                cities_visited=report_data.get('cities_visited', 0),
                favorite_weather=report_data.get('favorite_weather'),
                top_city=report_data.get('top_city'),
                max_temp=report_data.get('max_temp', 'N/A'),
                min_temp=report_data.get('min_temp', 'N/A'),
                common_condition=report_data.get('common_condition', 'N/A'),
                unsubscribe_url=f"{os.environ.get('BASE_URL', 'http://localhost:5000')}/unsubscribe/{user.id}",
                current_year=datetime.now().year
            )
            
            subject = f"Your Weekly Weather Report - {self.site_name}"
            
            return self._send_email(user.email, subject, html_body)
            
        except Exception as e:
            logging.error(f"Failed to send weekly report to {user.email}: {e}")
            return False
    
    def send_marketing_email(self, user, campaign_data):
        """Send marketing/promotional email"""
        try:
            template = Template(campaign_data['template'])
            
            html_body = template.render(
                site_name=self.site_name,
                user_name=user.first_name or user.username,
                base_url=os.environ.get('BASE_URL', 'http://localhost:5000'),
                unsubscribe_url=f"{os.environ.get('BASE_URL', 'http://localhost:5000')}/unsubscribe/{user.id}",
                current_year=datetime.now().year,
                **campaign_data.get('variables', {})
            )
            
            subject = campaign_data['subject']
            
            return self._send_email(user.email, subject, html_body)
            
        except Exception as e:
            logging.error(f"Failed to send marketing email to {user.email}: {e}")
            return False

# Email service instance - will be initialized in app context
email_service = None

def get_email_service():
    """Get email service instance"""
    global email_service
    if email_service is None:
        email_service = EmailService()
    return email_service

def send_bulk_emails(user_list, email_type, **kwargs):
    """Send bulk emails to a list of users"""
    success_count = 0
    
    for user in user_list:
        try:
            if email_type == 'welcome':
                success = email_service.send_welcome_email(user)
            elif email_type == 'weekly_report':
                success = email_service.send_weekly_report_email(user, kwargs.get('report_data', {}))
            elif email_type == 'marketing':
                success = email_service.send_marketing_email(user, kwargs.get('campaign_data', {}))
            else:
                continue
            
            if success:
                success_count += 1
                
        except Exception as e:
            logging.error(f"Failed to send {email_type} email to {user.email}: {e}")
    
    return success_count