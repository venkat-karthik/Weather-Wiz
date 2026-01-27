// Weather Animation System
class WeatherAnimations {
    constructor() {
        this.animationContainer = document.getElementById('weather-animation');
        this.animationElements = [];
        this.isAnimating = false;
        this.currentAnimation = null;
    }

    // Initialize animation based on weather condition
    initAnimation(condition, isDay = true) {
        console.log(`Initializing weather animation for condition: "${condition}", isDay: ${isDay}`);
        this.clearAnimations();
        
        const animationType = this.getAnimationType(condition, isDay);
        console.log(`Mapped to animation type: "${animationType}"`);
        this.startAnimation(animationType);
    }

    // Map weather conditions to animation types
    getAnimationType(condition, isDay) {
        // Normalize the condition string
        const normalizedCondition = condition ? condition.trim() : '';
        console.log(`Normalized condition: "${normalizedCondition}"`);
        
        const conditionMap = {
            // Clear conditions
            'Clear': isDay ? 'sun' : 'stars',
            'clear': isDay ? 'sun' : 'stars',
            
            // Cloud conditions
            'Clouds': 'clouds',
            'clouds': 'clouds',
            'Cloudy': 'clouds',
            'cloudy': 'clouds',
            'Overcast': 'clouds',
            'overcast': 'clouds',
            
            // Rain conditions
            'Rain': 'rain',
            'rain': 'rain',
            'Light Rain': 'drizzle',
            'light rain': 'drizzle',
            'Moderate Rain': 'rain',
            'moderate rain': 'rain',
            'Heavy Rain': 'rain',
            'heavy rain': 'rain',
            
            // Drizzle conditions
            'Drizzle': 'drizzle',
            'drizzle': 'drizzle',
            'Light Drizzle': 'drizzle',
            'light drizzle': 'drizzle',
            
            // Storm conditions
            'Thunderstorm': 'storm',
            'thunderstorm': 'storm',
            'Storm': 'storm',
            'storm': 'storm',
            'Thunder': 'storm',
            'thunder': 'storm',
            
            // Snow conditions
            'Snow': 'snow',
            'snow': 'snow',
            'Light Snow': 'snow',
            'light snow': 'snow',
            'Heavy Snow': 'snow',
            'heavy snow': 'snow',
            'Sleet': 'snow',
            'sleet': 'snow',
            
            // Fog/Mist conditions
            'Mist': 'fog',
            'mist': 'fog',
            'Fog': 'fog',
            'fog': 'fog',
            'Foggy': 'fog',
            'foggy': 'fog',
            
            // Haze conditions
            'Haze': 'haze',
            'haze': 'haze',
            'Hazy': 'haze',
            'hazy': 'haze',
            
            // Dust/Sand conditions
            'Dust': 'dust',
            'dust': 'dust',
            'Sand': 'dust',
            'sand': 'dust',
            
            // Smoke conditions
            'Smoke': 'smoke',
            'smoke': 'smoke',
            
            // Ash conditions
            'Ash': 'ash',
            'ash': 'ash',
            
            // Squall conditions
            'Squall': 'wind',
            'squall': 'wind',
            
            // Tornado conditions
            'Tornado': 'tornado',
            'tornado': 'tornado'
        };

        const animationType = conditionMap[normalizedCondition];
        if (!animationType) {
            console.warn(`Unknown weather condition: "${normalizedCondition}", falling back to default`);
            return isDay ? 'sun' : 'stars';
        }
        
        return animationType;
    }

    // Start specific animation
    startAnimation(type) {
        if (this.isAnimating) {
            this.clearAnimations();
        }

        this.isAnimating = true;
        this.currentAnimation = type;
        console.log(`Starting animation: ${type}`);

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
            case 'dust':
                this.createDustAnimation();
                break;
            case 'smoke':
                this.createSmokeAnimation();
                break;
            case 'ash':
                this.createAshAnimation();
                break;
            case 'wind':
                this.createWindAnimation();
                break;
            case 'tornado':
                this.createTornadoAnimation();
                break;
            default:
                console.warn(`Unknown animation type: ${type}, using default`);
                this.createDefaultAnimation();
        }
    }

    // Clear all animations
    clearAnimations() {
        this.isAnimating = false;
        this.currentAnimation = null;
        if (this.animationContainer) {
            this.animationContainer.innerHTML = '';
        }
        this.animationElements = [];
        
        // Remove any added CSS styles
        const existingStyles = document.querySelectorAll('style[data-weather-animation]');
        existingStyles.forEach(style => style.remove());
    }

    // Rain animation
    createRainAnimation() {
        const rainDrops = 200;
        
        for (let i = 0; i < rainDrops; i++) {
            const drop = document.createElement('div');
            drop.className = 'rain-drop';
            
            // Randomize properties for more realistic effect
            const speed = 0.5 + Math.random() * 0.8;
            const size = 1.5 + Math.random() * 1.5;
            const delay = Math.random() * 2;
            const xPos = Math.random() * window.innerWidth;
            const yPos = -50 - Math.random() * 100;
            
            drop.style.left = xPos + 'px';
            drop.style.top = yPos + 'px';
            drop.style.width = size + 'px';
            drop.style.height = (15 + size * 3) + 'px';
            drop.style.animationDuration = speed + 's';
            drop.style.animationDelay = delay + 's';
            
            this.animationContainer.appendChild(drop);
            this.animationElements.push(drop);
        }
        
        // Add some larger raindrops for variety
        for (let i = 0; i < 20; i++) {
            const drop = document.createElement('div');
            drop.className = 'rain-drop';
            
            const speed = 0.3 + Math.random() * 0.4;
            const size = 2.5 + Math.random() * 1;
            const delay = Math.random() * 3;
            const xPos = Math.random() * window.innerWidth;
            const yPos = -50 - Math.random() * 200;
            
            drop.style.left = xPos + 'px';
            drop.style.top = yPos + 'px';
            drop.style.width = size + 'px';
            drop.style.height = (20 + size * 4) + 'px';
            drop.style.animationDuration = speed + 's';
            drop.style.animationDelay = delay + 's';
            drop.style.opacity = '0.9';
            
            this.animationContainer.appendChild(drop);
            this.animationElements.push(drop);
        }
    }

    // Drizzle animation
    createDrizzleAnimation() {
        const drizzleDrops = 150;
        
        for (let i = 0; i < drizzleDrops; i++) {
            const drop = document.createElement('div');
            drop.className = 'drizzle-drop';
            
            const speed = 1.5 + Math.random() * 1;
            const delay = Math.random() * 3;
            const xPos = Math.random() * window.innerWidth;
            const yPos = -30 - Math.random() * 50;
            
            drop.style.left = xPos + 'px';
            drop.style.top = yPos + 'px';
            drop.style.animationDuration = speed + 's';
            drop.style.animationDelay = delay + 's';
            
            this.animationContainer.appendChild(drop);
            this.animationElements.push(drop);
        }
    }

    // Snow animation
    createSnowAnimation() {
        const snowflakes = 100;
        
        for (let i = 0; i < snowflakes; i++) {
            const flake = document.createElement('div');
            flake.className = 'snowflake';
            
            const speed = 3 + Math.random() * 4;
            const size = 4 + Math.random() * 6;
            const delay = Math.random() * 5;
            const xPos = Math.random() * window.innerWidth;
            const yPos = -50 - Math.random() * 100;
            
            flake.style.left = xPos + 'px';
            flake.style.top = yPos + 'px';
            flake.style.width = size + 'px';
            flake.style.height = size + 'px';
            flake.style.animationDuration = speed + 's';
            flake.style.animationDelay = delay + 's';
            
            this.animationContainer.appendChild(flake);
            this.animationElements.push(flake);
        }
        
        // Add some larger snowflakes
        for (let i = 0; i < 30; i++) {
            const flake = document.createElement('div');
            flake.className = 'snowflake';
            
            const speed = 4 + Math.random() * 3;
            const size = 8 + Math.random() * 4;
            const delay = Math.random() * 6;
            const xPos = Math.random() * window.innerWidth;
            const yPos = -50 - Math.random() * 150;
            
            flake.style.left = xPos + 'px';
            flake.style.top = yPos + 'px';
            flake.style.width = size + 'px';
            flake.style.height = size + 'px';
            flake.style.animationDuration = speed + 's';
            flake.style.animationDelay = delay + 's';
            flake.style.opacity = '0.9';
            
            this.animationContainer.appendChild(flake);
            this.animationElements.push(flake);
        }
    }

    // Storm animation
    createStormAnimation() {
        // Create rain first
        this.createRainAnimation();
        
        // Add lightning effects
        const lightningCount = 3;
        
        for (let i = 0; i < lightningCount; i++) {
            const lightning = document.createElement('div');
            lightning.className = 'lightning';
            
            const xPos = 100 + Math.random() * (window.innerWidth - 200);
            const delay = Math.random() * 4;
            
            lightning.style.left = xPos + 'px';
            lightning.style.top = '10%';
            lightning.style.animationDelay = delay + 's';
            
            this.animationContainer.appendChild(lightning);
            this.animationElements.push(lightning);
        }
        
        // Add darker cloud particles
        for (let i = 0; i < 50; i++) {
            const cloud = document.createElement('div');
            cloud.className = 'cloud-particle';
            
            const size = 20 + Math.random() * 40;
            const speed = 8 + Math.random() * 6;
            const delay = Math.random() * 5;
            const yPos = Math.random() * 30;
            
            cloud.style.width = size + 'px';
            cloud.style.height = size + 'px';
            cloud.style.top = yPos + '%';
            cloud.style.animationDuration = speed + 's';
            cloud.style.animationDelay = delay + 's';
            cloud.style.background = 'rgba(100, 100, 100, 0.6)';
            
            this.animationContainer.appendChild(cloud);
            this.animationElements.push(cloud);
        }
    }

    // Cloud animation
    createCloudAnimation() {
        // Create multiple cloud layers
        const cloudLayers = [
            { count: 8, size: 60, speed: 15, yPos: 10, opacity: 0.8 },
            { count: 12, size: 40, speed: 12, yPos: 25, opacity: 0.6 },
            { count: 15, size: 30, speed: 10, yPos: 40, opacity: 0.4 }
        ];
        
        cloudLayers.forEach(layer => {
            for (let i = 0; i < layer.count; i++) {
                const cloud = document.createElement('div');
                cloud.className = 'cloud-shape';
                
                const size = layer.size + Math.random() * 20;
                const speed = layer.speed + Math.random() * 5;
                const delay = Math.random() * 10;
                const xPos = -200 - Math.random() * 300;
                
                cloud.style.width = size + 'px';
                cloud.style.height = (size * 0.6) + 'px';
                cloud.style.top = layer.yPos + Math.random() * 10 + '%';
                cloud.style.left = xPos + 'px';
                cloud.style.animationDuration = speed + 's';
                cloud.style.animationDelay = delay + 's';
                cloud.style.opacity = layer.opacity;
                
                // Add cloud details
                cloud.style.setProperty('--cloud-size', size + 'px');
                
                this.animationContainer.appendChild(cloud);
                this.animationElements.push(cloud);
            }
        });
        
        // Add some floating cloud particles
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'cloud-particle';
            
            const size = 15 + Math.random() * 25;
            const speed = 8 + Math.random() * 6;
            const delay = Math.random() * 8;
            const yPos = Math.random() * 60;
            
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.top = yPos + '%';
            particle.style.animationDuration = speed + 's';
            particle.style.animationDelay = delay + 's';
            
            this.animationContainer.appendChild(particle);
            this.animationElements.push(particle);
        }
    }

    // Sun animation
    createSunAnimation() {
        const sun = document.createElement('div');
        sun.className = 'sun';
        
        // Add sun rays
        for (let i = 0; i < 8; i++) {
            const ray = document.createElement('div');
            ray.style.position = 'absolute';
            ray.style.width = '4px';
            ray.style.height = '30px';
            ray.style.background = 'rgba(255, 215, 0, 0.6)';
            ray.style.top = '-35px';
            ray.style.left = '50%';
            ray.style.transformOrigin = '2px 65px';
            ray.style.transform = `translateX(-50%) rotate(${i * 45}deg)`;
            ray.style.animation = 'sun-pulse 3s ease-in-out infinite';
            ray.style.animationDelay = (i * 0.1) + 's';
            
            sun.appendChild(ray);
        }
        
        this.animationContainer.appendChild(sun);
        this.animationElements.push(sun);
        
        // Add some warm glow particles
        for (let i = 0; i < 20; i++) {
            const glow = document.createElement('div');
            glow.style.position = 'absolute';
            glow.style.width = '3px';
            glow.style.height = '3px';
            glow.style.background = 'rgba(255, 215, 0, 0.4)';
            glow.style.borderRadius = '50%';
            glow.style.animation = 'sun-glow 4s ease-in-out infinite';
            glow.style.animationDelay = Math.random() * 4 + 's';
            
            const angle = Math.random() * 360;
            const distance = 100 + Math.random() * 50;
            const x = Math.cos(angle * Math.PI / 180) * distance;
            const y = Math.sin(angle * Math.PI / 180) * distance;
            
            glow.style.left = `calc(90% + ${x}px)`;
            glow.style.top = `calc(10% + ${y}px)`;
            
            this.animationContainer.appendChild(glow);
            this.animationElements.push(glow);
        }
    }

    // Stars animation
    createStarAnimation() {
        const starCount = 150;
        
        for (let i = 0; i < starCount; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            
            const xPos = Math.random() * window.innerWidth;
            const yPos = Math.random() * (window.innerHeight * 0.7);
            const size = 1 + Math.random() * 2;
            const delay = Math.random() * 3;
            const duration = 1.5 + Math.random() * 1;
            
            star.style.left = xPos + 'px';
            star.style.top = yPos + 'px';
            star.style.width = size + 'px';
            star.style.height = size + 'px';
            star.style.animationDuration = duration + 's';
            star.style.animationDelay = delay + 's';
            
            this.animationContainer.appendChild(star);
            this.animationElements.push(star);
        }
        
        // Add some larger, brighter stars
        for (let i = 0; i < 20; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            
            const xPos = Math.random() * window.innerWidth;
            const yPos = Math.random() * (window.innerHeight * 0.6);
            const size = 3 + Math.random() * 2;
            const delay = Math.random() * 4;
            const duration = 2 + Math.random() * 1;
            
            star.style.left = xPos + 'px';
            star.style.top = yPos + 'px';
            star.style.width = size + 'px';
            star.style.height = size + 'px';
            star.style.animationDuration = duration + 's';
            star.style.animationDelay = delay + 's';
            star.style.opacity = '0.9';
            star.style.boxShadow = '0 0 6px rgba(255, 255, 255, 0.9)';
            
            this.animationContainer.appendChild(star);
            this.animationElements.push(star);
        }
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

    // Dust animation
    createDustAnimation() {
        const dustParticles = 100;
        
        for (let i = 0; i < dustParticles; i++) {
            const particle = document.createElement('div');
            particle.className = 'dust-particle';
            const size = 1 + Math.random() * 3;
            const speed = 8 + Math.random() * 12;
            const opacity = 0.1 + Math.random() * 0.3;
            
            particle.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                background: rgba(139,69,19,${opacity});
                border-radius: 50%;
                left: ${Math.random() * 120}%;
                animation: dustFloat ${speed}s linear infinite;
                animation-delay: ${Math.random() * 5}s;
                filter: blur(0.5px);
            `;
            
            this.animationContainer.appendChild(particle);
            this.animationElements.push(particle);
        }

        // Add dust clouds
        for (let i = 0; i < 4; i++) {
            const dustCloud = document.createElement('div');
            dustCloud.className = 'dust-cloud';
            dustCloud.style.cssText = `
                position: absolute;
                width: 200px;
                height: 100px;
                background: radial-gradient(ellipse, rgba(139,69,19,0.1), transparent);
                top: ${20 + i * 20}%;
                left: -200px;
                animation: dustCloudMove ${10 + Math.random() * 10}s linear infinite;
                animation-delay: ${i * 2}s;
            `;
            
            this.animationContainer.appendChild(dustCloud);
            this.animationElements.push(dustCloud);
        }

        this.addCSS(`
            @keyframes dustFloat {
                0% {
                    top: -10px;
                    opacity: 0;
                    transform: translateX(0px) rotate(0deg);
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
                    transform: translateX(${Math.random() * 100 - 50}px) rotate(360deg);
                }
            }
            @keyframes dustCloudMove {
                0% {
                    left: -200px;
                    opacity: 0;
                }
                20% {
                    opacity: 1;
                }
                80% {
                    opacity: 1;
                }
                100% {
                    left: calc(100% + 200px);
                    opacity: 0;
                }
            }
        `);
    }

    // Smoke animation
    createSmokeAnimation() {
        const smokeParticles = 50;
        
        for (let i = 0; i < smokeParticles; i++) {
            const smoke = document.createElement('div');
            smoke.className = 'smoke-particle';
            const size = 20 + Math.random() * 40;
            const speed = 6 + Math.random() * 8;
            const opacity = 0.05 + Math.random() * 0.15;
            
            smoke.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                background: radial-gradient(circle, rgba(128,128,128,${opacity}), transparent);
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                animation: smokeRise ${speed}s ease-out infinite;
                animation-delay: ${Math.random() * 3}s;
                filter: blur(2px);
            `;
            
            this.animationContainer.appendChild(smoke);
            this.animationElements.push(smoke);
        }

        // Add smoke plumes
        for (let i = 0; i < 3; i++) {
            const plume = document.createElement('div');
            plume.className = 'smoke-plume';
            plume.style.cssText = `
                position: absolute;
                width: 60px;
                height: 200px;
                background: linear-gradient(to top, 
                    rgba(128,128,128,0.2), 
                    rgba(128,128,128,0.1), 
                    transparent
                );
                bottom: -200px;
                left: ${30 + i * 20}%;
                animation: smokePlume ${8 + Math.random() * 4}s ease-out infinite;
                animation-delay: ${i * 1.5}s;
                border-radius: 30px 30px 0 0;
            `;
            
            this.animationContainer.appendChild(plume);
            this.animationElements.push(plume);
        }

        this.addCSS(`
            @keyframes smokeRise {
                0% {
                    bottom: -50px;
                    opacity: 0;
                    transform: scale(0.5) translateX(0px);
                }
                20% {
                    opacity: 1;
                }
                80% {
                    opacity: 1;
                }
                100% {
                    bottom: 100vh;
                    opacity: 0;
                    transform: scale(2) translateX(${Math.random() * 100 - 50}px);
                }
            }
            @keyframes smokePlume {
                0% {
                    height: 0px;
                    opacity: 0;
                }
                30% {
                    opacity: 1;
                }
                100% {
                    height: 300px;
                    opacity: 0;
                }
            }
        `);
    }

    // Ash animation
    createAshAnimation() {
        const ashParticles = 80;
        
        for (let i = 0; i < ashParticles; i++) {
            const ash = document.createElement('div');
            ash.className = 'ash-particle';
            ash.innerHTML = '●';
            const size = 3 + Math.random() * 6;
            const speed = 4 + Math.random() * 6;
            const opacity = 0.3 + Math.random() * 0.7;
            
            ash.style.cssText = `
                position: absolute;
                color: rgba(64,64,64,${opacity});
                font-size: ${size}px;
                left: ${Math.random() * 110}%;
                animation: ashFall ${speed}s linear infinite;
                animation-delay: ${Math.random() * 4}s;
                filter: blur(0.3px);
            `;
            
            this.animationContainer.appendChild(ash);
            this.animationElements.push(ash);
        }

        // Add ash clouds
        for (let i = 0; i < 2; i++) {
            const ashCloud = document.createElement('div');
            ashCloud.className = 'ash-cloud';
            ashCloud.style.cssText = `
                position: absolute;
                width: 300px;
                height: 150px;
                background: radial-gradient(ellipse, rgba(64,64,64,0.15), transparent);
                top: ${10 + i * 30}%;
                left: -300px;
                animation: ashCloudMove ${12 + Math.random() * 8}s linear infinite;
                animation-delay: ${i * 3}s;
            `;
            
            this.animationContainer.appendChild(ashCloud);
            this.animationElements.push(ashCloud);
        }

        this.addCSS(`
            @keyframes ashFall {
                0% {
                    top: -20px;
                    opacity: 0;
                    transform: translateX(0px) rotate(0deg);
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
                    transform: translateX(${Math.random() * 60 - 30}px) rotate(720deg);
                }
            }
            @keyframes ashCloudMove {
                0% {
                    left: -300px;
                    opacity: 0;
                }
                20% {
                    opacity: 1;
                }
                80% {
                    opacity: 1;
                }
                100% {
                    left: calc(100% + 300px);
                    opacity: 0;
                }
            }
        `);
    }

    // Wind animation
    createWindAnimation() {
        // Create wind lines
        for (let i = 0; i < 15; i++) {
            const windLine = document.createElement('div');
            windLine.className = 'wind-line';
            const length = 80 + Math.random() * 120;
            const speed = 1 + Math.random() * 2;
            const opacity = 0.1 + Math.random() * 0.3;
            
            windLine.style.cssText = `
                position: absolute;
                width: ${length}px;
                height: 1px;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(255,255,255,${opacity}), 
                    rgba(255,255,255,${opacity * 1.5}), 
                    rgba(255,255,255,${opacity}), 
                    transparent
                );
                top: ${Math.random() * 80}%;
                left: -${length}px;
                animation: windMove ${speed}s linear infinite;
                animation-delay: ${Math.random() * 3}s;
            `;
            
            this.animationContainer.appendChild(windLine);
            this.animationElements.push(windLine);
        }

        // Add wind swirls
        for (let i = 0; i < 5; i++) {
            const swirl = document.createElement('div');
            swirl.className = 'wind-swirl';
            swirl.innerHTML = '🌀';
            const size = 20 + Math.random() * 30;
            const speed = 3 + Math.random() * 4;
            
            swirl.style.cssText = `
                position: absolute;
                color: rgba(255,255,255,0.3);
                font-size: ${size}px;
                top: ${Math.random() * 70}%;
                left: ${Math.random() * 100}%;
                animation: windSwirl ${speed}s linear infinite;
                animation-delay: ${Math.random() * 2}s;
            `;
            
            this.animationContainer.appendChild(swirl);
            this.animationElements.push(swirl);
        }

        this.addCSS(`
            @keyframes windMove {
                0% {
                    left: -100px;
                    opacity: 0;
                }
                20% {
                    opacity: 1;
                }
                80% {
                    opacity: 1;
                }
                100% {
                    left: calc(100% + 100px);
                    opacity: 0;
                }
            }
            @keyframes windSwirl {
                0% {
                    transform: scale(0.5) rotate(0deg);
                    opacity: 0;
                }
                20% {
                    opacity: 1;
                }
                80% {
                    opacity: 1;
                }
                100% {
                    transform: scale(1.5) rotate(360deg);
                    opacity: 0;
                }
            }
        `);
    }

    // Tornado animation
    createTornadoAnimation() {
        // Create tornado funnel
        const tornado = document.createElement('div');
        tornado.className = 'tornado-funnel';
        tornado.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 300px;
            background: linear-gradient(to top, 
                rgba(64,64,64,0.8), 
                rgba(128,128,128,0.6), 
                rgba(192,192,192,0.4), 
                transparent
            );
            transform: translate(-50%, -50%);
            animation: tornadoSpin 2s linear infinite;
            border-radius: 10px;
            filter: blur(1px);
        `;
        
        this.animationContainer.appendChild(tornado);
        this.animationElements.push(tornado);

        // Create debris
        for (let i = 0; i < 30; i++) {
            const debris = document.createElement('div');
            debris.className = 'tornado-debris';
            debris.innerHTML = ['●', '◆', '▲', '■', '★'][Math.floor(Math.random() * 5)];
            const size = 4 + Math.random() * 8;
            const speed = 1 + Math.random() * 2;
            
            debris.style.cssText = `
                position: absolute;
                color: rgba(64,64,64,0.8);
                font-size: ${size}px;
                top: 50%;
                left: 50%;
                animation: debrisSpin ${speed}s linear infinite;
                animation-delay: ${Math.random() * 2}s;
                transform-origin: 0 0;
            `;
            
            this.animationContainer.appendChild(debris);
            this.animationElements.push(debris);
        }

        // Add wind effects around tornado
        for (let i = 0; i < 8; i++) {
            const windEffect = document.createElement('div');
            windEffect.className = 'tornado-wind';
            windEffect.style.cssText = `
                position: absolute;
                width: 100px;
                height: 2px;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(255,255,255,0.2), 
                    transparent
                );
                top: ${30 + i * 8}%;
                left: 50%;
                transform: translateX(-50%);
                animation: tornadoWind ${1.5 + Math.random()}s linear infinite;
                animation-delay: ${i * 0.2}s;
            `;
            
            this.animationContainer.appendChild(windEffect);
            this.animationElements.push(windEffect);
        }

        this.addCSS(`
            @keyframes tornadoSpin {
                0% {
                    transform: translate(-50%, -50%) rotate(0deg);
                }
                100% {
                    transform: translate(-50%, -50%) rotate(360deg);
                }
            }
            @keyframes debrisSpin {
                0% {
                    transform: rotate(0deg) translateX(20px) rotate(0deg);
                }
                100% {
                    transform: rotate(360deg) translateX(20px) rotate(-360deg);
                }
            }
            @keyframes tornadoWind {
                0% {
                    transform: translateX(-50%) scaleX(0);
                    opacity: 0;
                }
                50% {
                    opacity: 1;
                }
                100% {
                    transform: translateX(-50%) scaleX(2);
                    opacity: 0;
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
        style.setAttribute('data-weather-animation', 'true');
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
