// Weather Animation System
class WeatherAnimations {
    constructor() {
        this.animationContainer = document.getElementById('weather-animation');
        this.animationElements = [];
        this.isAnimating = false;
    }

    // Initialize animation based on weather condition
    initAnimation(condition, isDay = true) {
        this.clearAnimations();
        
        const animationType = this.getAnimationType(condition, isDay);
        this.startAnimation(animationType);
    }

    // Map weather conditions to animation types
    getAnimationType(condition, isDay) {
        const conditionMap = {
            'Clear': isDay ? 'sun' : 'stars',
            'Clouds': 'clouds',
            'Rain': 'rain',
            'Drizzle': 'drizzle',
            'Thunderstorm': 'storm',
            'Snow': 'snow',
            'Mist': 'fog',
            'Fog': 'fog',
            'Haze': 'haze'
        };

        return conditionMap[condition] || (isDay ? 'sun' : 'stars');
    }

    // Start specific animation
    startAnimation(type) {
        if (this.isAnimating) {
            this.clearAnimations();
        }

        this.isAnimating = true;

        switch (type) {
            case 'rain':
                this.createRainAnimation();
                break;
            case 'drizzle':
                this.createDrizzleAnimation();
                break;
            case 'snow':
                this.createSnowAnimation();
                break;
            case 'storm':
                this.createStormAnimation();
                break;
            case 'clouds':
                this.createCloudAnimation();
                break;
            case 'sun':
                this.createSunAnimation();
                break;
            case 'stars':
                this.createStarAnimation();
                break;
            case 'fog':
                this.createFogAnimation();
                break;
            case 'haze':
                this.createHazeAnimation();
                break;
            default:
                this.createDefaultAnimation();
        }
    }

    // Clear all animations
    clearAnimations() {
        this.isAnimating = false;
        if (this.animationContainer) {
            this.animationContainer.innerHTML = '';
        }
        this.animationElements = [];
    }

    // Rain animation
    createRainAnimation() {
        const rainDrops = 100;
        
        for (let i = 0; i < rainDrops; i++) {
            const drop = document.createElement('div');
            drop.className = 'rain-drop';
            drop.style.cssText = `
                position: absolute;
                width: 2px;
                height: 20px;
                background: linear-gradient(transparent, rgba(255,255,255,0.3), rgba(255,255,255,0.8));
                left: ${Math.random() * 100}%;
                animation: rainFall ${0.5 + Math.random() * 0.5}s linear infinite;
                animation-delay: ${Math.random() * 2}s;
            `;
            
            this.animationContainer.appendChild(drop);
            this.animationElements.push(drop);
        }

        // Add rain animation keyframes
        this.addCSS(`
            @keyframes rainFall {
                0% {
                    top: -20px;
                    opacity: 1;
                }
                100% {
                    top: 100vh;
                    opacity: 0.3;
                }
            }
        `);
    }

    // Drizzle animation (lighter rain)
    createDrizzleAnimation() {
        const drizzleDrops = 50;
        
        for (let i = 0; i < drizzleDrops; i++) {
            const drop = document.createElement('div');
            drop.className = 'drizzle-drop';
            drop.style.cssText = `
                position: absolute;
                width: 1px;
                height: 15px;
                background: linear-gradient(transparent, rgba(255,255,255,0.2), rgba(255,255,255,0.5));
                left: ${Math.random() * 100}%;
                animation: drizzleFall ${1 + Math.random() * 1}s linear infinite;
                animation-delay: ${Math.random() * 3}s;
            `;
            
            this.animationContainer.appendChild(drop);
            this.animationElements.push(drop);
        }

        this.addCSS(`
            @keyframes drizzleFall {
                0% {
                    top: -15px;
                    opacity: 0.8;
                }
                100% {
                    top: 100vh;
                    opacity: 0.1;
                }
            }
        `);
    }

    // Snow animation
    createSnowAnimation() {
        const snowflakes = 50;
        
        for (let i = 0; i < snowflakes; i++) {
            const flake = document.createElement('div');
            flake.className = 'snowflake';
            flake.innerHTML = '❄';
            flake.style.cssText = `
                position: absolute;
                color: rgba(255,255,255,0.8);
                font-size: ${8 + Math.random() * 8}px;
                left: ${Math.random() * 100}%;
                animation: snowFall ${3 + Math.random() * 3}s linear infinite;
                animation-delay: ${Math.random() * 3}s;
            `;
            
            this.animationContainer.appendChild(flake);
            this.animationElements.push(flake);
        }

        this.addCSS(`
            @keyframes snowFall {
                0% {
                    top: -20px;
                    transform: translateX(0px) rotate(0deg);
                }
                100% {
                    top: 100vh;
                    transform: translateX(${Math.random() * 100 - 50}px) rotate(360deg);
                }
            }
        `);
    }

    // Storm animation (rain + lightning)
    createStormAnimation() {
        // Create rain first
        this.createRainAnimation();
        
        // Add lightning flashes
        const lightning = document.createElement('div');
        lightning.className = 'lightning';
        lightning.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.1);
            animation: lightning 4s infinite;
        `;
        
        this.animationContainer.appendChild(lightning);
        this.animationElements.push(lightning);

        this.addCSS(`
            @keyframes lightning {
                0%, 90%, 92%, 94%, 96%, 100% {
                    opacity: 0;
                }
                91%, 93%, 95% {
                    opacity: 1;
                }
            }
        `);
    }

    // Cloud animation
    createCloudAnimation() {
        const cloudCount = 5;
        
        for (let i = 0; i < cloudCount; i++) {
            const cloud = document.createElement('div');
            cloud.className = 'cloud';
            cloud.innerHTML = '☁';
            cloud.style.cssText = `
                position: absolute;
                color: rgba(255,255,255,0.3);
                font-size: ${30 + Math.random() * 20}px;
                top: ${Math.random() * 40}%;
                left: -50px;
                animation: cloudFloat ${20 + Math.random() * 10}s linear infinite;
                animation-delay: ${Math.random() * 5}s;
            `;
            
            this.animationContainer.appendChild(cloud);
            this.animationElements.push(cloud);
        }

        this.addCSS(`
            @keyframes cloudFloat {
                0% {
                    left: -50px;
                }
                100% {
                    left: calc(100% + 50px);
                }
            }
        `);
    }

    // Sun animation
    createSunAnimation() {
        const sun = document.createElement('div');
        sun.className = 'sun';
        sun.style.cssText = `
            position: absolute;
            top: 10%;
            right: 10%;
            width: 80px;
            height: 80px;
            background: radial-gradient(circle, rgba(255,223,0,0.8), rgba(255,165,0,0.4), transparent);
            border-radius: 50%;
            animation: sunGlow 3s ease-in-out infinite alternate;
        `;
        
        this.animationContainer.appendChild(sun);
        this.animationElements.push(sun);

        this.addCSS(`
            @keyframes sunGlow {
                0% {
                    box-shadow: 0 0 20px rgba(255,223,0,0.5);
                    transform: scale(1);
                }
                100% {
                    box-shadow: 0 0 40px rgba(255,223,0,0.8);
                    transform: scale(1.1);
                }
            }
        `);
    }

    // Stars animation
    createStarAnimation() {
        const starCount = 30;
        
        for (let i = 0; i < starCount; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.innerHTML = '✦';
            star.style.cssText = `
                position: absolute;
                color: rgba(255,255,255,0.6);
                font-size: ${4 + Math.random() * 8}px;
                top: ${Math.random() * 60}%;
                left: ${Math.random() * 100}%;
                animation: starTwinkle ${1 + Math.random() * 2}s ease-in-out infinite alternate;
                animation-delay: ${Math.random() * 3}s;
            `;
            
            this.animationContainer.appendChild(star);
            this.animationElements.push(star);
        }

        this.addCSS(`
            @keyframes starTwinkle {
                0% {
                    opacity: 0.3;
                    transform: scale(0.8);
                }
                100% {
                    opacity: 1;
                    transform: scale(1.2);
                }
            }
        `);
    }

    // Fog animation
    createFogAnimation() {
        const fogLayers = 3;
        
        for (let i = 0; i < fogLayers; i++) {
            const fog = document.createElement('div');
            fog.className = 'fog-layer';
            fog.style.cssText = `
                position: absolute;
                top: ${30 + i * 20}%;
                left: -20%;
                width: 140%;
                height: 20%;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(255,255,255,0.1), 
                    rgba(255,255,255,0.2), 
                    rgba(255,255,255,0.1), 
                    transparent
                );
                animation: fogMove ${15 + i * 5}s linear infinite;
                animation-delay: ${i * 2}s;
            `;
            
            this.animationContainer.appendChild(fog);
            this.animationElements.push(fog);
        }

        this.addCSS(`
            @keyframes fogMove {
                0% {
                    transform: translateX(-10%);
                }
                100% {
                    transform: translateX(10%);
                }
            }
        `);
    }

    // Haze animation
    createHazeAnimation() {
        const haze = document.createElement('div');
        haze.className = 'haze';
        haze.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(180deg, 
                transparent 0%, 
                rgba(255,255,255,0.1) 30%, 
                rgba(255,255,255,0.2) 70%, 
                transparent 100%
            );
            animation: hazeFloat 5s ease-in-out infinite alternate;
        `;
        
        this.animationContainer.appendChild(haze);
        this.animationElements.push(haze);

        this.addCSS(`
            @keyframes hazeFloat {
                0% {
                    opacity: 0.5;
                }
                100% {
                    opacity: 0.8;
                }
            }
        `);
    }

    // Default animation for unknown conditions
    createDefaultAnimation() {
        // Simple ambient effect
        const ambient = document.createElement('div');
        ambient.className = 'ambient';
        ambient.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 50% 50%, 
                rgba(255,255,255,0.05) 0%, 
                transparent 70%
            );
            animation: ambientPulse 4s ease-in-out infinite alternate;
        `;
        
        this.animationContainer.appendChild(ambient);
        this.animationElements.push(ambient);

        this.addCSS(`
            @keyframes ambientPulse {
                0% {
                    opacity: 0.3;
                }
                100% {
                    opacity: 0.7;
                }
            }
        `);
    }

    // Helper method to add CSS animations
    addCSS(css) {
        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }
}

// Global instance
const weatherAnimations = new WeatherAnimations();

// Global function to initialize weather animation
function initWeatherAnimation(condition, isDay = true) {
    if (weatherAnimations) {
        weatherAnimations.initAnimation(condition, isDay);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WeatherAnimations;
}
