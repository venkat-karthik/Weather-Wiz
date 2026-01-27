// Global function to toggle theme (for onclick handlers)
function toggleTheme() {
    if (window.themeManager) {
        window.themeManager.toggleTheme();
    } else {
        // Fallback if theme manager isn't initialized yet
        const currentTheme = localStorage.getItem('weather-app-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        // Apply theme directly
        document.body.className = document.body.className.replace(/theme-\w+/, `theme-${newTheme}`);
        localStorage.setItem('weather-app-theme', newTheme);
        
        // Update button text
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
        }
    }
}

// Theme Toggle Functionality
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('weather-app-theme') || 'light';
        this.themeToggle = document.getElementById('theme-toggle');
        this.themeIcon = document.getElementById('theme-icon');
        
        this.init();
    }

    init() {
        // Set initial theme
        this.applyTheme(this.currentTheme);
        
        // Add event listener to toggle button
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }

        // Update icon based on current theme
        this.updateIcon();
        
        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!localStorage.getItem('weather-app-theme')) {
                    this.applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        this.saveTheme(newTheme);
    }

    applyTheme(theme) {
        this.currentTheme = theme;
        document.body.className = document.body.className.replace(/theme-\w+/, `theme-${theme}`);
        
        // Update theme color meta tag for mobile browsers
        const themeColorMeta = document.querySelector('meta[name="theme-color"]');
        if (themeColorMeta) {
            themeColorMeta.content = theme === 'dark' ? '#0F1419' : '#64B5F6';
        } else {
            const meta = document.createElement('meta');
            meta.name = 'theme-color';
            meta.content = theme === 'dark' ? '#0F1419' : '#64B5F6';
            document.getElementsByTagName('head')[0].appendChild(meta);
        }

        this.updateIcon();
        this.updateBackgroundGradient(theme);
    }

    updateIcon() {
        if (this.themeIcon) {
            // Use feather icons data attribute to change icon
            if (this.currentTheme === 'dark') {
                this.themeIcon.setAttribute('data-feather', 'moon');
                this.themeToggle.setAttribute('title', 'Switch to Light Mode');
            } else {
                this.themeIcon.setAttribute('data-feather', 'sun');
                this.themeToggle.setAttribute('title', 'Switch to Dark Mode');
            }
            
            // Re-render feather icons
            if (typeof feather !== 'undefined') {
                feather.replace();
            }
        }
        
        // Update button text for simple theme toggle buttons
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.textContent = this.currentTheme === 'dark' ? '☀️' : '🌙';
        }
    }

    updateBackgroundGradient(theme) {
        // Update CSS custom properties for smooth transition
        const root = document.documentElement;
        
        if (theme === 'dark') {
            root.style.setProperty('--bg-gradient-start', '#0F1419');
            root.style.setProperty('--bg-gradient-end', '#1A2332');
        } else {
            root.style.setProperty('--bg-gradient-start', '#64B5F6');
            root.style.setProperty('--bg-gradient-end', '#E1F5FE');
        }
    }

    saveTheme(theme) {
        localStorage.setItem('weather-app-theme', theme);
    }

    getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    // Auto-detect theme based on time of day
    getTimeBasedTheme() {
        const hour = new Date().getHours();
        return (hour >= 6 && hour < 20) ? 'light' : 'dark';
    }

    // Set theme based on weather condition
    setWeatherBasedTheme(condition, isDay) {
        let suggestedTheme;
        
        if (!isDay) {
            suggestedTheme = 'dark';
        } else {
            switch (condition) {
                case 'Thunderstorm':
                case 'Rain':
                case 'Drizzle':
                    suggestedTheme = 'dark';
                    break;
                case 'Snow':
                case 'Mist':
                case 'Fog':
                    suggestedTheme = 'dark';
                    break;
                case 'Clear':
                case 'Clouds':
                default:
                    suggestedTheme = 'light';
                    break;
            }
        }

        // Only apply if user hasn't manually set a preference
        if (!localStorage.getItem('weather-app-theme-manual')) {
            this.applyTheme(suggestedTheme);
        }
    }

    // Mark theme as manually set
    setManualTheme(theme) {
        this.applyTheme(theme);
        this.saveTheme(theme);
        localStorage.setItem('weather-app-theme-manual', 'true');
    }

    // Reset to auto theme selection
    resetToAutoTheme() {
        localStorage.removeItem('weather-app-theme-manual');
        localStorage.removeItem('weather-app-theme');
        const autoTheme = this.getSystemTheme();
        this.applyTheme(autoTheme);
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.themeManager = new ThemeManager();
});

// Global function to set weather-based theme
function setWeatherTheme(condition, isDay) {
    if (window.themeManager) {
        window.themeManager.setWeatherBasedTheme(condition, isDay);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
