// Main Application JavaScript
class WeatherApp {
    constructor() {
        this.refreshInterval = null;
        this.updateInterval = 600000; // 10 minutes
        this.isOnline = navigator.onLine;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupAutoRefresh();
        this.setupOfflineHandling();
        this.setupServiceWorker();
        this.initializeFeatherIcons();
    }

    setupEventListeners() {
        // Global click handlers
        document.addEventListener('click', (e) => {
            // Handle refresh buttons
            if (e.target.matches('[data-refresh]')) {
                e.preventDefault();
                this.refreshWeatherData();
            }

            // Handle unit toggle buttons
            if (e.target.matches('[data-unit-toggle]')) {
                e.preventDefault();
                this.toggleTemperatureUnit();
            }

            // Handle city quick-select
            if (e.target.matches('[data-city]')) {
                e.preventDefault();
                const city = e.target.dataset.city;
                this.switchCity(city);
            }
        });

        // Form submission handlers
        document.addEventListener('submit', (e) => {
            if (e.target.matches('.search-form')) {
                this.handleSearchSubmit(e);
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + R for refresh
            if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
                e.preventDefault();
                this.refreshWeatherData();
            }

            // T for theme toggle
            if (e.key === 't' || e.key === 'T') {
                if (!e.target.matches('input, textarea')) {
                    e.preventDefault();
                    if (window.themeManager) {
                        window.themeManager.toggleTheme();
                    }
                }
            }
        });

        // Handle online/offline status
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.showNotification('Connection restored', 'success');
            this.refreshWeatherData();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showNotification('No internet connection', 'warning');
        });

        // Handle visibility change (tab switching)
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && this.isOnline) {
                // Refresh data when tab becomes visible
                this.refreshWeatherData();
            }
        });
    }

    setupAutoRefresh() {
        // Clear existing interval
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        // Set up auto-refresh
        this.refreshInterval = setInterval(() => {
            if (this.isOnline && !document.hidden) {
                this.refreshWeatherData();
            }
        }, this.updateInterval);
    }

    setupOfflineHandling() {
        // Check if page was loaded offline
        if (!this.isOnline) {
            this.showNotification('Offline mode - showing cached data', 'info');
        }
    }

    setupServiceWorker() {
        // Register service worker for offline functionality
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        }
    }

    initializeFeatherIcons() {
        // Initialize Feather icons when they're loaded
        if (typeof feather !== 'undefined') {
            feather.replace();
        } else {
            // Wait for feather to load
            const checkFeather = () => {
                if (typeof feather !== 'undefined') {
                    feather.replace();
                } else {
                    setTimeout(checkFeather, 100);
                }
            };
            checkFeather();
        }
    }

    refreshWeatherData() {
        if (!this.isOnline) {
            this.showNotification('Cannot refresh - no internet connection', 'warning');
            return;
        }

        // Show loading state
        this.setLoadingState(true);

        // Get current page and city
        const currentCity = this.getCurrentCity();
        const currentPage = window.location.pathname;

        // Construct refresh URL
        let refreshUrl = currentPage;
        if (currentCity) {
            const separator = currentPage.includes('?') ? '&' : '?';
            refreshUrl += `${separator}city=${encodeURIComponent(currentCity)}`;
        }

        // Reload the page to refresh data
        window.location.href = refreshUrl;
    }

    getCurrentCity() {
        // Try to extract city from various sources
        const urlParams = new URLSearchParams(window.location.search);
        let city = urlParams.get('city');

        if (!city) {
            // Try to get from dropdown
            const cityDropdown = document.getElementById('cityDropdown');
            if (cityDropdown) {
                city = cityDropdown.textContent.trim();
            }
        }

        if (!city) {
            // Try to get from page content
            const locationElement = document.querySelector('.location-name, .city-name');
            if (locationElement) {
                city = locationElement.textContent.split(',')[0].trim();
            }
        }

        return city;
    }

    switchCity(cityName) {
        const currentPage = window.location.pathname;
        const newUrl = `${currentPage}?city=${encodeURIComponent(cityName)}`;
        window.location.href = newUrl;
    }

    toggleTemperatureUnit() {
        const tempElements = document.querySelectorAll('[data-temp-celsius]');
        const currentUnit = localStorage.getItem('weather-temp-unit') || 'celsius';
        const newUnit = currentUnit === 'celsius' ? 'fahrenheit' : 'celsius';
        
        tempElements.forEach(element => {
            const celsius = parseFloat(element.dataset.tempCelsius);
            const fahrenheit = parseFloat(element.dataset.tempFahrenheit);
            const tempValue = element.querySelector('.temp-value');
            const tempUnitSpan = element.querySelector('.temp-unit');
            
            if (tempValue && tempUnitSpan) {
                if (newUnit === 'fahrenheit') {
                    tempValue.textContent = fahrenheit;
                    tempUnitSpan.textContent = 'F';
                } else {
                    tempValue.textContent = celsius;
                    tempUnitSpan.textContent = 'C';
                }
            }
        });
        
        // Update other temperature displays
        document.querySelectorAll('[data-temp-value]').forEach(element => {
            const celsius = parseFloat(element.dataset.tempValue);
            if (!isNaN(celsius)) {
                if (newUnit === 'fahrenheit') {
                    const fahrenheit = Math.round((celsius * 9/5) + 32);
                    element.textContent = `${fahrenheit}°F`;
                } else {
                    element.textContent = `${celsius}°C`;
                }
            }
        });
        
        localStorage.setItem('weather-temp-unit', newUnit);
        this.showNotification(`Temperature unit changed to °${newUnit === 'celsius' ? 'C' : 'F'}`, 'success');
    }

    handleSearchSubmit(e) {
        const form = e.target;
        const formData = new FormData(form);
        const cityName = formData.get('city_name');

        if (!cityName || !cityName.trim()) {
            e.preventDefault();
            this.showNotification('Please enter a city name', 'warning');
            return;
        }

        // Show loading state
        this.setLoadingState(true);
    }

    setLoadingState(loading) {
        const body = document.body;
        if (loading) {
            body.classList.add('loading');
        } else {
            body.classList.remove('loading');
        }

        // Update refresh buttons
        const refreshButtons = document.querySelectorAll('[data-refresh]');
        refreshButtons.forEach(button => {
            const icon = button.querySelector('[data-feather="refresh-cw"]');
            if (icon) {
                if (loading) {
                    icon.style.animation = 'spin 1s linear infinite';
                } else {
                    icon.style.animation = '';
                }
            }
        });
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show notification`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 300px;
            animation: slideInRight 0.3s ease-out;
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.classList.remove('show');
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }
        }, 5000);

        // Add animation styles if not already added
        if (!document.querySelector('#notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                .notification {
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                }
            `;
            document.head.appendChild(style);
        }
    }

    // Utility method to format timestamps
    formatTime(timestamp) {
        return new Date(timestamp * 1000).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Utility method to format dates
    formatDate(timestamp) {
        return new Date(timestamp * 1000).toLocaleDateString('en-US', {
            weekday: 'long',
            month: 'short',
            day: 'numeric'
        });
    }

    // Method to handle geolocation
    getCurrentLocation() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation is not supported'));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                position => {
                    resolve({
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    });
                },
                error => {
                    reject(error);
                },
                {
                    timeout: 10000,
                    enableHighAccuracy: true
                }
            );
        });
    }

    // Method to get weather for current location
    async getWeatherForCurrentLocation() {
        try {
            const location = await this.getCurrentLocation();
            const url = `/api/weather-by-coords?lat=${location.lat}&lon=${location.lon}`;
            window.location.href = url;
        } catch (error) {
            this.showNotification('Unable to get your location', 'error');
        }
    }

    // Clean up
    destroy() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.weatherApp = new WeatherApp();
    
    // Add current location button functionality
    const locationButtons = document.querySelectorAll('[data-location]');
    locationButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            window.weatherApp.getWeatherForCurrentLocation();
        });
    });
});

// Clean up on page unload
window.addEventListener('beforeunload', function() {
    if (window.weatherApp) {
        window.weatherApp.destroy();
    }
});

// Global utility functions
window.weatherUtils = {
    formatTime: (timestamp) => {
        return new Date(timestamp * 1000).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    formatDate: (timestamp) => {
        return new Date(timestamp * 1000).toLocaleDateString('en-US', {
            weekday: 'long',
            month: 'short',
            day: 'numeric'
        });
    },
    
    getWindDirection: (degrees) => {
        const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
        return directions[Math.round(degrees / 45) % 8];
    },
    
    getUVLevel: (index) => {
        if (index <= 2) return 'Low';
        if (index <= 5) return 'Moderate';
        if (index <= 7) return 'High';
        if (index <= 10) return 'Very High';
        return 'Extreme';
    },
    
    getAQILevel: (aqi) => {
        const levels = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor'];
        return levels[aqi - 1] || 'Unknown';
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WeatherApp;
}
