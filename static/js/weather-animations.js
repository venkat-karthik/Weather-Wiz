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
        const rainDrops = 150;
        
        for (let i = 0; i < rainDrops; i++) {
            const drop = document.createElement('div');
            drop.className = 'rain-drop';
            const speed = 0.3 + Math.random() * 0.4;
            const size = 1.5 + Math.random() * 1;
            const opacity = 0.4 + Math.random() * 0.6;
            
            drop.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${15 + Math.random() * 10}px;
                background: linear-gradient(transparent, rgba(135,206,235,${opacity}), rgba(255,255,255,${opacity + 0.2}));
                left: ${Math.random() * 110}%;
                animation: rainFall ${speed}s linear infinite;
                animation-delay: ${Math.random() * 2}s;
                transform: rotate(${10 + Math.random() * 5}deg);
                border-radius: 0 0 50% 50%;
            `;
            
            this.animationContainer.appendChild(drop);
            this.animationElements.push(drop);
        }

        // Add wind effect
        for (let i = 0; i < 3; i++) {
            const wind = document.createElement('div');
            wind.className = 'wind-line';
            wind.style.cssText = `
                position: absolute;
                width: 100px;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                top: ${20 + i * 30}%;
                left: -100px;
                animation: windMove ${2 + Math.random()}s linear infinite;
                animation-delay: ${i * 0.5}s;
            `;
            this.animationContainer.appendChild(wind);
            this.animationElements.push(wind);
        }

        this.addCSS(`
            @keyframes rainFall {
                0% {
                    top: -30px;
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                90% {
                    opacity: 1;
                }
                100% {
                    top: 100vh;
                    opacity: 0;
                }
            }
            @keyframes windMove {
                0% {
                    left: -100px;
                    opacity: 0;
                }
                50% {
                    opacity: 1;
                }
                100% {
                    left: calc(100% + 100px);
                    opacity: 0;
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
        const cloudCount = 8;
        
        for (let i = 0; i < cloudCount; i++) {
            const cloud = document.createElement('div');
            cloud.className = 'cloud';
            const size = 20 + Math.random() * 30;
            const opacity = 0.2 + Math.random() * 0.4;
            const speed = 15 + Math.random() * 20;
            
            cloud.style.cssText = `
                position: absolute;
                width: ${size * 2}px;
                height: ${size}px;
                background: rgba(255,255,255,${opacity});
                border-radius: ${size}px;
                top: ${Math.random() * 60}%;
                left: -${size * 2}px;
                animation: cloudFloat ${speed}s linear infinite;
                animation-delay: ${Math.random() * 8}s;
                box-shadow: 
                    ${size * 0.5}px 0 0 -${size * 0.2}px rgba(255,255,255,${opacity * 0.8}),
                    -${size * 0.5}px 0 0 -${size * 0.2}px rgba(255,255,255,${opacity * 0.8}),
                    0 ${size * 0.3}px 0 -${size * 0.3}px rgba(255,255,255,${opacity * 0.6});
            `;
            
            // Add subtle vertical movement
            cloud.style.animation += `, cloudBob ${3 + Math.random() * 2}s ease-in-out infinite alternate`;
            
            this.animationContainer.appendChild(cloud);
            this.animationElements.push(cloud);
        }

        this.addCSS(`
            @keyframes cloudFloat {
                0% {
                    left: -100px;
                    transform: translateY(0);
                }
                100% {
                    left: calc(100% + 100px);
                    transform: translateY(0);
                }
            }
            @keyframes cloudBob {
                0% {
                    transform: translateY(0px);
                }
                100% {
                    transform: translateY(-10px);
                }
            }
        `);
    }

    // Sun animation
    createSunAnimation() {
        // Main sun
        const sun = document.createElement('div');
        sun.className = 'sun';
        sun.style.cssText = `
            position: absolute;
            top: 10%;
            right: 10%;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(255,223,0,0.9), rgba(255,165,0,0.6), rgba(255,140,0,0.3), transparent);
            border-radius: 50%;
            animation: sunGlow 4s ease-in-out infinite alternate, sunRotate 20s linear infinite;
        `;
        
        // Sun rays
        for (let i = 0; i < 12; i++) {
            const ray = document.createElement('div');
            ray.className = 'sun-ray';
            const angle = (i * 30) * Math.PI / 180;
            const length = 40 + Math.random() * 20;
            
            ray.style.cssText = `
                position: absolute;
                top: calc(10% + 50px);
                right: calc(10% + 50px);
                width: 3px;
                height: ${length}px;
                background: linear-gradient(rgba(255,223,0,0.8), transparent);
                transform-origin: 1.5px 0;
                transform: rotate(${i * 30}deg) translateY(-60px);
                animation: rayPulse ${2 + Math.random()}s ease-in-out infinite alternate;
                animation-delay: ${i * 0.1}s;
                border-radius: 2px;
            `;
            
            this.animationContainer.appendChild(ray);
            this.animationElements.push(ray);
        }
        
        // Sun sparkles
        for (let i = 0; i < 6; i++) {
            const sparkle = document.createElement('div');
            sparkle.className = 'sun-sparkle';
            sparkle.innerHTML = '✦';
            sparkle.style.cssText = `
                position: absolute;
                color: rgba(255,223,0,0.7);
                font-size: ${8 + Math.random() * 6}px;
                top: ${8 + Math.random() * 15}%;
                right: ${8 + Math.random() * 15}%;
                animation: sparkle ${1 + Math.random() * 2}s ease-in-out infinite alternate;
                animation-delay: ${Math.random() * 2}s;
            `;
            
            this.animationContainer.appendChild(sparkle);
            this.animationElements.push(sparkle);
        }
        
        this.animationContainer.appendChild(sun);
        this.animationElements.push(sun);

        this.addCSS(`
            @keyframes sunGlow {
                0% {
                    box-shadow: 0 0 30px rgba(255,223,0,0.6), 0 0 60px rgba(255,165,0,0.4);
                    transform: scale(1);
                }
                100% {
                    box-shadow: 0 0 50px rgba(255,223,0,0.9), 0 0 100px rgba(255,165,0,0.6);
                    transform: scale(1.05);
                }
            }
            @keyframes sunRotate {
                0% {
                    transform: rotate(0deg);
                }
                100% {
                    transform: rotate(360deg);
                }
            }
            @keyframes rayPulse {
                0% {
                    opacity: 0.3;
                    transform: rotate(var(--ray-angle, 0deg)) translateY(-60px) scale(1);
                }
                100% {
                    opacity: 0.8;
                    transform: rotate(var(--ray-angle, 0deg)) translateY(-60px) scale(1.2);
                }
            }
            @keyframes sparkle {
                0% {
                    opacity: 0.4;
                    transform: scale(0.8) rotate(0deg);
                }
                100% {
                    opacity: 1;
                    transform: scale(1.2) rotate(180deg);
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
