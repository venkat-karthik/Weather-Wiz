#!/bin/bash

# Weather Wiz Deployment Script
# This script sets up the production environment

set -e  # Exit on any error

echo "🚀 Starting Weather Wiz deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p uploads
mkdir -p ssl
mkdir -p logs
mkdir -p backups

# Set proper permissions
chmod 755 uploads
chmod 700 ssl
chmod 755 logs
chmod 700 backups

# Generate SSL certificates if they don't exist
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    print_status "Generating self-signed SSL certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=WeatherWiz/CN=localhost"
    print_warning "Using self-signed certificates. Replace with proper SSL certificates for production."
fi

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found. Please create it with the required environment variables."
    exit 1
fi

# Validate required environment variables
print_status "Validating environment variables..."
required_vars=("OPENWEATHER_API_KEY" "SECRET_KEY" "DATABASE_URL")
for var in "${required_vars[@]}"; do
    if ! grep -q "^${var}=" .env; then
        print_error "Required environment variable ${var} not found in .env file"
        exit 1
    fi
done

# Build and start services
print_status "Building Docker images..."
docker-compose build

print_status "Starting services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 30

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    print_success "Services are running!"
else
    print_error "Some services failed to start. Check logs with: docker-compose logs"
    exit 1
fi

# Run database migrations
print_status "Running database migrations..."
docker-compose exec web flask db upgrade

# Create admin user (optional)
read -p "Do you want to create an admin user? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Creating admin user..."
    docker-compose exec web python -c "
from app import app, db
from models import User
with app.app_context():
    admin = User(
        email='admin@weatherwiz.com',
        username='admin',
        first_name='Admin',
        is_premium=True
    )
    admin.set_password('admin123')  # Change this password!
    db.session.add(admin)
    db.session.commit()
    print('Admin user created: admin@weatherwiz.com / admin123')
"
    print_warning "Please change the admin password after first login!"
fi

# Setup log rotation
print_status "Setting up log rotation..."
sudo tee /etc/logrotate.d/weatherwiz > /dev/null <<EOF
$(pwd)/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $(whoami) $(whoami)
    postrotate
        docker-compose restart web
    endscript
}
EOF

# Create backup script
print_status "Creating backup script..."
cat > backup.sh << 'EOF'
#!/bin/bash
# Weather Wiz Backup Script

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create database backup
docker-compose exec -T db pg_dump -U weather_user weather_wiz > "${BACKUP_DIR}/db_backup_${DATE}.sql"

# Create uploads backup
tar -czf "${BACKUP_DIR}/uploads_backup_${DATE}.tar.gz" uploads/

# Keep only last 7 days of backups
find "${BACKUP_DIR}" -name "*.sql" -mtime +7 -delete
find "${BACKUP_DIR}" -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: ${DATE}"
EOF

chmod +x backup.sh

# Setup cron job for backups
print_status "Setting up daily backups..."
(crontab -l 2>/dev/null; echo "0 2 * * * $(pwd)/backup.sh >> $(pwd)/logs/backup.log 2>&1") | crontab -

# Create monitoring script
print_status "Creating monitoring script..."
cat > monitor.sh << 'EOF'
#!/bin/bash
# Weather Wiz Monitoring Script

# Check if services are running
if ! docker-compose ps | grep -q "Up"; then
    echo "Services are down! Restarting..."
    docker-compose up -d
fi

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Warning: Disk usage is at ${DISK_USAGE}%"
fi

# Check memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')
if [ $MEMORY_USAGE -gt 80 ]; then
    echo "Warning: Memory usage is at ${MEMORY_USAGE}%"
fi

# Health check
if ! curl -f http://localhost/health > /dev/null 2>&1; then
    echo "Health check failed! Restarting web service..."
    docker-compose restart web
fi
EOF

chmod +x monitor.sh

# Setup monitoring cron job
(crontab -l 2>/dev/null; echo "*/5 * * * * $(pwd)/monitor.sh >> $(pwd)/logs/monitor.log 2>&1") | crontab -

# Display final information
print_success "Deployment completed successfully!"
echo
echo "🌟 Weather Wiz is now running!"
echo
echo "📊 Service URLs:"
echo "   • Main site: https://localhost"
echo "   • Health check: https://localhost/health"
echo "   • Admin panel: https://localhost/admin/products"
echo
echo "🔧 Management commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart services: docker-compose restart"
echo "   • Run backup: ./backup.sh"
echo "   • Check monitoring: ./monitor.sh"
echo
echo "📁 Important directories:"
echo "   • Logs: ./logs/"
echo "   • Backups: ./backups/"
echo "   • SSL certificates: ./ssl/"
echo "   • Uploads: ./uploads/"
echo
print_warning "Next steps:"
echo "1. Replace self-signed SSL certificates with proper ones"
echo "2. Update environment variables for production"
echo "3. Configure domain name and DNS"
echo "4. Set up external monitoring (optional)"
echo "5. Configure email settings for notifications"
echo
print_success "Happy weather forecasting! 🌤️"