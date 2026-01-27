# Weather Wiz - Production Deployment Checklist

## 🚀 Pre-Deployment Checklist

### 1. Environment Configuration
- [ ] Update `.env` file with production values
- [ ] Set `FLASK_ENV=production`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure production database URL (PostgreSQL recommended)
- [ ] Set up Redis for caching and sessions
- [ ] Configure SMTP settings for email notifications
- [ ] Add your Amazon affiliate tag
- [ ] Set up Sentry DSN for error tracking
- [ ] Configure Google Analytics ID (optional)

### 2. Security Configuration
- [ ] Enable HTTPS/SSL certificates
- [ ] Update security headers in production
- [ ] Configure firewall rules
- [ ] Set up rate limiting with Redis
- [ ] Enable CSRF protection
- [ ] Configure session security settings
- [ ] Set up backup encryption keys

### 3. Database Setup
- [ ] Install PostgreSQL (recommended for production)
- [ ] Create production database
- [ ] Run database migrations: `flask db upgrade`
- [ ] Create admin user account
- [ ] Initialize system settings
- [ ] Set up database backups

### 4. Infrastructure Setup
- [ ] Configure reverse proxy (Nginx recommended)
- [ ] Set up SSL/TLS certificates (Let's Encrypt recommended)
- [ ] Configure load balancer (if needed)
- [ ] Set up monitoring and alerting
- [ ] Configure log rotation
- [ ] Set up automated backups

### 5. Application Deployment
- [ ] Install production dependencies
- [ ] Configure Gunicorn or uWSGI
- [ ] Set up systemd service files
- [ ] Configure static file serving
- [ ] Set up Celery for background tasks
- [ ] Test all application features
- [ ] Verify email functionality

### 6. Monitoring and Analytics
- [ ] Set up system monitoring (CPU, memory, disk)
- [ ] Configure application performance monitoring
- [ ] Set up log aggregation
- [ ] Configure alerting for critical issues
- [ ] Test backup and restore procedures
- [ ] Set up uptime monitoring

### 7. Content and Data
- [ ] Add real Amazon affiliate products
- [ ] Configure weather API limits
- [ ] Set up content delivery network (CDN)
- [ ] Optimize images and static assets
- [ ] Configure caching strategies

## 📋 Production Environment Variables

```bash
# Application
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key-here
BASE_URL=https://yourdomain.com

# Database
DATABASE_URL=postgresql://username:password@localhost/weather_wiz

# Redis
REDIS_URL=redis://localhost:6379/0

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourdomain.com

# API Keys
OPENWEATHER_API_KEY=your-openweather-api-key
AMAZON_AFFILIATE_TAG=your-affiliate-tag-20

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
GOOGLE_ANALYTICS_ID=your-ga-id-here

# Security
ENABLE_REGISTRATION=true
ENABLE_EMAIL_VERIFICATION=true
ENABLE_ANALYTICS=true
ENABLE_AFFILIATE_TRACKING=true

# File Uploads
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/var/www/weather-wiz/uploads
```

## 🐳 Docker Deployment

### Quick Start with Docker Compose
```bash
# 1. Clone repository
git clone <your-repo-url>
cd weather-wiz

# 2. Update environment variables
cp .env.example .env
# Edit .env with your production values

# 3. Deploy with Docker Compose
docker-compose up -d

# 4. Run database migrations
docker-compose exec web flask db upgrade

# 5. Create admin user
docker-compose exec web python -c "
from app import app, db
from models import User
with app.app_context():
    admin = User(email='admin@yourdomain.com', username='admin', is_premium=True)
    admin.set_password('your-secure-password')
    db.session.add(admin)
    db.session.commit()
"
```

## 🔧 Manual Deployment (Ubuntu/Debian)

### 1. System Dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx
```

### 2. Application Setup
```bash
# Create application user
sudo useradd -m -s /bin/bash weatherwiz
sudo su - weatherwiz

# Clone and setup application
git clone <your-repo-url> weather-wiz
cd weather-wiz
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with production values

# Run database migrations
export FLASK_APP=app.py
flask db upgrade
```

### 3. Systemd Service
Create `/etc/systemd/system/weather-wiz.service`:
```ini
[Unit]
Description=Weather Wiz Web Application
After=network.target

[Service]
User=weatherwiz
Group=weatherwiz
WorkingDirectory=/home/weatherwiz/weather-wiz
Environment=PATH=/home/weatherwiz/weather-wiz/venv/bin
ExecStart=/home/weatherwiz/weather-wiz/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Nginx Configuration
Create `/etc/nginx/sites-available/weather-wiz`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/weatherwiz/weather-wiz/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 5. Start Services
```bash
sudo systemctl enable weather-wiz
sudo systemctl start weather-wiz
sudo systemctl enable nginx
sudo systemctl restart nginx
```

## 📊 Post-Deployment Verification

### 1. Health Checks
- [ ] Application loads at your domain
- [ ] HTTPS certificate is valid
- [ ] Database connections work
- [ ] Redis caching is functional
- [ ] Email sending works
- [ ] Weather API integration works
- [ ] Affiliate links are properly formatted

### 2. Performance Tests
- [ ] Page load times are acceptable
- [ ] API endpoints respond quickly
- [ ] Database queries are optimized
- [ ] Static files are served efficiently
- [ ] Caching is working properly

### 3. Security Tests
- [ ] Security headers are present
- [ ] HTTPS is enforced
- [ ] Rate limiting is active
- [ ] Input validation works
- [ ] Authentication is secure
- [ ] Admin access is restricted

### 4. Monitoring Setup
- [ ] System metrics are being collected
- [ ] Application logs are being captured
- [ ] Error tracking is working
- [ ] Uptime monitoring is active
- [ ] Backup procedures are tested

## 🔄 Maintenance Tasks

### Daily
- [ ] Check system health dashboard
- [ ] Review error logs
- [ ] Monitor resource usage
- [ ] Verify backup completion

### Weekly
- [ ] Review analytics reports
- [ ] Update affiliate products
- [ ] Check security alerts
- [ ] Test backup restoration

### Monthly
- [ ] Update dependencies
- [ ] Review performance metrics
- [ ] Optimize database
- [ ] Security audit

## 🆘 Troubleshooting

### Common Issues
1. **Application won't start**: Check logs in `/var/log/weather-wiz/`
2. **Database connection errors**: Verify DATABASE_URL and PostgreSQL service
3. **Email not sending**: Check SMTP configuration and credentials
4. **Static files not loading**: Verify Nginx configuration and file permissions
5. **High memory usage**: Check for memory leaks and optimize queries

### Useful Commands
```bash
# Check application status
sudo systemctl status weather-wiz

# View application logs
sudo journalctl -u weather-wiz -f

# Check Nginx status
sudo systemctl status nginx

# Test Nginx configuration
sudo nginx -t

# Restart services
sudo systemctl restart weather-wiz nginx

# Database backup
python maintenance.py backup

# View system metrics
python maintenance.py report
```

## 📞 Support

For deployment support and troubleshooting:
1. Check the application logs first
2. Review this checklist for missed steps
3. Consult the monitoring dashboard
4. Check system resource usage

Remember to keep your deployment secure and regularly updated! 🔒