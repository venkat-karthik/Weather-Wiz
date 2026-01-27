// Voice Assistant for Weather App
class WeatherVoiceAssistant {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.isSpeaking = false;
        this.weatherService = null;
        this.currentCity = 'London';
        
        this.init();
    }

    init() {
        // Initialize speech recognition
        this.initSpeechRecognition();
        
        // Initialize text-to-speech
        this.initTextToSpeech();
        
        // Get weather service reference
        this.weatherService = window.weatherService;
        
        console.log('Voice Assistant initialized');
    }

    initSpeechRecognition() {
        // Check if browser supports speech recognition
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('Speech recognition not supported');
            return;
        }

        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure recognition settings for better accuracy
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 3; // Get multiple alternatives for better accuracy

        // Set up event handlers
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI();
            console.log('Listening...');
        };

        this.recognition.onresult = (event) => {
            const result = event.results[0];
            const transcript = result[0].transcript.toLowerCase();
            const confidence = result[0].confidence;
            
            console.log('Heard:', transcript);
            console.log('Confidence:', confidence);
            
            // Log all alternatives for debugging
            if (result.length > 1) {
                console.log('All alternatives:');
                for (let i = 0; i < result.length; i++) {
                    console.log(`  ${i + 1}: "${result[i].transcript}" (confidence: ${result[i].confidence})`);
                }
            }
            
            // Use the most confident result
            this.processVoiceCommand(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.updateUI();
            
            if (event.error === 'no-speech') {
                this.speak('I didn\'t hear anything. Please try again.');
            } else if (event.error === 'audio-capture') {
                this.speak('I couldn\'t access your microphone. Please check your microphone settings.');
            } else if (event.error === 'not-allowed') {
                this.speak('Microphone access was denied. Please allow microphone access and try again.');
            } else {
                this.speak('There was an error with speech recognition. Please try again.');
            }
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.updateUI();
            console.log('Recognition ended');
        };
    }

    initTextToSpeech() {
        // Check if browser supports speech synthesis
        if (!('speechSynthesis' in window)) {
            console.error('Speech synthesis not supported');
            return;
        }

        // Configure speech synthesis
        this.synthesis.cancel(); // Clear any existing speech
    }

    startListening() {
        if (!this.recognition) {
            this.speak('Speech recognition is not supported in this browser.');
            return;
        }

        if (this.isListening) {
            this.stopListening();
            return;
        }

        try {
            this.recognition.start();
            this.speak('Listening...');
        } catch (error) {
            console.error('Error starting recognition:', error);
            this.speak('Sorry, I couldn\'t start listening. Please try again.');
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }

    speak(text) {
        if (!this.synthesis) {
            console.error('Speech synthesis not supported');
            return;
        }

        // Cancel any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        // Set voice (prefer female voice if available)
        const voices = this.synthesis.getVoices();
        const preferredVoice = voices.find(voice => 
            voice.lang.includes('en') && voice.name.includes('Female')
        ) || voices.find(voice => voice.lang.includes('en')) || voices[0];
        
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        utterance.onstart = () => {
            this.isSpeaking = true;
            this.updateUI();
        };

        utterance.onend = () => {
            this.isSpeaking = false;
            this.updateUI();
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
            this.isSpeaking = false;
            this.updateUI();
        };

        this.synthesis.speak(utterance);
    }

    processVoiceCommand(transcript) {
        console.log('=== VOICE COMMAND PROCESSING ===');
        console.log('Raw transcript:', transcript);
        console.log('Transcript length:', transcript.length);

        // Weather queries
        if (this.isWeatherQuery(transcript)) {
            console.log('Detected weather query');
            this.handleWeatherQuery(transcript);
            return;
        }

        // Help command
        if (transcript.includes('help') || transcript.includes('what can you do')) {
            console.log('Detected help command');
            this.speak('I can help you with weather information. Try asking things like "What\'s the weather in London?" or "How\'s the weather tomorrow?"');
            return;
        }

        // Test command for debugging
        if (transcript.includes('test') || transcript.includes('debug')) {
            console.log('Detected test command');
            this.speak(`I heard: "${transcript}". This is a test of the voice recognition system.`);
            return;
        }

        // Stop listening command
        if (transcript.includes('stop') || transcript.includes('goodbye') || transcript.includes('bye')) {
            console.log('Detected stop command');
            this.speak('Goodbye! Have a great day!');
            return;
        }

        // Unknown command
        console.log('Unknown command detected');
        this.speak(`I heard: "${transcript}". I didn\'t understand that. Try asking about the weather or say "help" for assistance.`);
    }

    isWeatherQuery(transcript) {
        const weatherKeywords = [
            'weather', 'temperature', 'forecast', 'rain', 'snow', 'sunny', 'cloudy',
            'hot', 'cold', 'warm', 'cool', 'humid', 'windy', 'storm'
        ];

        return weatherKeywords.some(keyword => transcript.includes(keyword));
    }

    async handleWeatherQuery(transcript) {
        // Extract city name
        const city = this.extractCity(transcript);
        
        if (!city) {
            this.speak('I couldn\'t identify a city. Please try asking again with a specific city name.');
            return;
        }

        // Extract time reference
        const timeRef = this.extractTimeReference(transcript);
        
        try {
            this.speak(`Getting weather information for ${city}...`);
            
            // Get weather data
            const weatherData = await this.getWeatherData(city, timeRef);
            
            if (weatherData) {
                const response = this.formatWeatherResponse(weatherData, timeRef);
                this.speak(response);
                
                // Update the UI if we have the weather service
                if (this.weatherService) {
                    this.updateWeatherUI(weatherData);
                }
            } else {
                this.speak(`Sorry, I couldn't get weather information for ${city}. Please try again.`);
            }
        } catch (error) {
            console.error('Error getting weather data:', error);
            this.speak('Sorry, there was an error getting the weather information. Please try again.');
        }
    }

    extractCity(transcript) {
        console.log('Transcript for city extraction:', transcript);

        // Clean the transcript first
        let cleanTranscript = transcript.toLowerCase().trim();
        
        // Remove common prefixes and suffixes that might be misheard
        const prefixesToRemove = [
            'what is the weather in',
            'what\'s the weather in',
            'how is the weather in',
            'tell me the weather in',
            'give me the weather in',
            'show me the weather in',
            'check the weather in',
            'what is the weather for',
            'what\'s the weather for',
            'how is the weather for',
            'tell me the weather for',
            'give me the weather for',
            'show me the weather for',
            'check the weather for',
            'weather in',
            'weather for',
            'weather of',
            'weather at',
            'forecast in',
            'forecast for',
            'forecast of',
            'forecast at',
            'temperature in',
            'temperature for',
            'temperature of',
            'temperature at',
            'is the weather in',
            'is the weather for',
            'is the weather of',
            'is the weather at',
            'the weather in',
            'the weather for',
            'the weather of',
            'the weather at',
            'listening weather forecast of',
            'listening weather forecast for',
            'listening weather forecast in',
            'listening weather forecast at',
            'listening',
            'in',
            'for',
            'of',
            'at',
            'the',
            'is',
            'what',
            'how',
            'tell',
            'give',
            'show',
            'check',
            'me',
            'please',
            'thanks',
            'thank you'
        ];

        // Remove prefixes
        for (const prefix of prefixesToRemove) {
            if (cleanTranscript.startsWith(prefix + ' ')) {
                cleanTranscript = cleanTranscript.substring(prefix.length + 1);
                break;
            }
        }

        // Remove suffixes
        const suffixesToRemove = [
            ' weather',
            ' forecast',
            ' temperature',
            ' today',
            ' tomorrow',
            ' tonight',
            ' morning',
            ' afternoon',
            ' evening',
            ' night',
            ' now',
            ' please',
            ' thanks',
            ' thank you',
            ' .',
            ' ?',
            ' !'
        ];

        for (const suffix of suffixesToRemove) {
            if (cleanTranscript.endsWith(suffix)) {
                cleanTranscript = cleanTranscript.substring(0, cleanTranscript.length - suffix.length);
            }
        }

        console.log('Cleaned transcript:', cleanTranscript);

        // If we have a clean city name, validate it
        if (cleanTranscript && this.isValidCityName(cleanTranscript)) {
            const mappedCity = this.mapCityName(cleanTranscript);
            console.log('Found valid city from cleaned transcript:', cleanTranscript, '->', mappedCity);
            return mappedCity;
        }

        // Strategy 2: Look for specific patterns
        const patterns = [
            /(?:in|for|of|at)\s+([a-zA-Z\s-]+?)(?:\s+(?:weather|forecast|temperature|today|tomorrow|tonight|morning|afternoon|evening|night|now|please|thanks|thank you|\.|\?|!|$))?$/i,
            /(?:weather|forecast|temperature)\s+(?:in|for|of|at)\s+([a-zA-Z\s-]+?)(?:\s+(?:today|tomorrow|tonight|morning|afternoon|evening|night|now|please|thanks|thank you|\.|\?|!|$))?$/i,
            /(?:what|how|tell|give|show|check)\s+(?:is|me|the)\s+(?:weather|forecast|temperature)\s+(?:in|for|of|at)\s+([a-zA-Z\s-]+?)(?:\s+(?:today|tomorrow|tonight|morning|afternoon|evening|night|now|please|thanks|thank you|\.|\?|!|$))?$/i
        ];

        for (const pattern of patterns) {
            const match = transcript.match(pattern);
            if (match && match[1]) {
                const potentialCity = match[1].trim();
                if (this.isValidCityName(potentialCity)) {
                    const mappedCity = this.mapCityName(potentialCity);
                    console.log('Found city using pattern:', potentialCity, '->', mappedCity);
                    return mappedCity;
                }
            }
        }

        // Strategy 3: Extract words and find the most likely city name
        const words = transcript.toLowerCase().split(/\s+/);
        const weatherWords = ['weather', 'forecast', 'temperature', 'ecast', 'orecast', 'emperature'];
        const fillerWords = ['the', 'is', 'in', 'for', 'of', 'at', 'what', 'how', 'tell', 'give', 'show', 'me', 'please', 'thanks', 'thank', 'you', 'today', 'tomorrow', 'tonight', 'morning', 'afternoon', 'evening', 'night', 'now', 'this', 'that', 'a', 'to', 'up', 'about', 'want', 'need', 'get', 'check', 'look', 'listening'];

        // Filter out weather and filler words
        const filteredWords = words.filter(word => 
            !weatherWords.includes(word) && 
            !fillerWords.includes(word) &&
            word.length > 1 &&
            /^[a-zA-Z-]+$/.test(word) // Only letters and hyphens
        );

        console.log('Filtered words:', filteredWords);

        // Try combinations of filtered words
        if (filteredWords.length > 0) {
            // Try single words first
            for (const word of filteredWords) {
                if (this.isValidCityName(word)) {
                    const mappedCity = this.mapCityName(word);
                    console.log('Found single word city:', word, '->', mappedCity);
                    return mappedCity;
                }
            }

            // Try 2-word combinations
            for (let i = 0; i < filteredWords.length - 1; i++) {
                const twoWordCity = filteredWords[i] + ' ' + filteredWords[i + 1];
                if (this.isValidCityName(twoWordCity)) {
                    const mappedCity = this.mapCityName(twoWordCity);
                    console.log('Found two-word city:', twoWordCity, '->', mappedCity);
                    return mappedCity;
                }
            }

            // Try 3-word combinations
            for (let i = 0; i < filteredWords.length - 2; i++) {
                const threeWordCity = filteredWords[i] + ' ' + filteredWords[i + 1] + ' ' + filteredWords[i + 2];
                if (this.isValidCityName(threeWordCity)) {
                    const mappedCity = this.mapCityName(threeWordCity);
                    console.log('Found three-word city:', threeWordCity, '->', mappedCity);
                    return mappedCity;
                }
            }

            // If no valid combination found, return the first filtered word as fallback
            const mappedCity = this.mapCityName(filteredWords[0]);
            console.log('Using first filtered word as fallback:', filteredWords[0], '->', mappedCity);
            return mappedCity;
        }

        // Strategy 4: Look for any word that could be a city name
        for (const word of words) {
            if (word.length >= 2 && /^[a-zA-Z]+$/.test(word) && !fillerWords.includes(word)) {
                const mappedCity = this.mapCityName(word);
                console.log('Using individual word as fallback:', word, '->', mappedCity);
                return mappedCity;
            }
        }

        console.log('No valid city found, falling back to current city:', this.currentCity);
        return this.currentCity;
    }
    
    isValidCityName(city) {
        if (!city || city.length < 2 || city.length > 50) {
            return false;
        }
        
        // Must contain only letters, spaces, and hyphens
        if (!/^[a-zA-Z\s-]+$/.test(city)) {
            return false;
        }
        
        // Must not be just common words
        const invalidWords = [
            'weather', 'forecast', 'temperature', 'ecast', 'orecast', 'emperature',
            'in', 'for', 'at', 'of', 'the', 'is', 'a', 'to', 'me', 'how', 'what',
            'tell', 'give', 'show', 'check', 'look', 'up', 'about', 'want', 'need',
            'get', 'please', 'thanks', 'thank', 'you', 'today', 'tomorrow', 'tonight',
            'morning', 'afternoon', 'evening', 'night', 'now', 'this', 'that',
            'and', 'or', 'but', 'so', 'if', 'then', 'else', 'when', 'where', 'why',
            'who', 'which', 'that', 'these', 'those', 'my', 'your', 'his', 'her',
            'their', 'our', 'its', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'shall'
        ];
        
        const cityLower = city.toLowerCase().trim();
        
        // Check if it's exactly an invalid word
        if (invalidWords.includes(cityLower)) {
            return false;
        }
        
        // Check if it starts or ends with invalid words
        const cityWords = cityLower.split(/\s+/);
        if (cityWords.length > 0) {
            const firstWord = cityWords[0];
            const lastWord = cityWords[cityWords.length - 1];
            
            if (invalidWords.includes(firstWord) || invalidWords.includes(lastWord)) {
                return false;
            }
        }
        
        // Check if it contains invalid words in the middle (but allow them as part of city names)
        // This is more permissive - we only reject if the entire phrase is invalid
        const allWordsInvalid = cityWords.every(word => invalidWords.includes(word));
        if (allWordsInvalid && cityWords.length > 0) {
            return false;
        }
        
        // Additional validation: must have at least one word that's not in the invalid list
        const hasValidWord = cityWords.some(word => !invalidWords.includes(word));
        if (!hasValidWord) {
            return false;
        }
        
        return true;
    }

    extractTimeReference(transcript) {
        if (transcript.includes('tomorrow')) {
            return 'tomorrow';
        } else if (transcript.includes('tonight') || transcript.includes('evening') || transcript.includes('night')) {
            return 'tonight';
        } else if (transcript.includes('morning')) {
            return 'morning';
        } else if (transcript.includes('afternoon')) {
            return 'afternoon';
        } else if (transcript.includes('today')) {
            return 'today';
        }
        return 'current';
    }

    async getWeatherData(city, timeRef) {
        try {
            // Use the existing weather service if available
            if (this.weatherService && this.weatherService.getCurrentWeather) {
                const weatherData = await this.weatherService.getCurrentWeather(city);
                return weatherData;
            }

            // Fallback: make direct API call
            const response = await fetch(`/api/weather/${encodeURIComponent(city)}`);
            if (response.ok) {
                return await response.json();
            }
            
            return null;
        } catch (error) {
            console.error('Error fetching weather data:', error);
            return null;
        }
    }

    formatWeatherResponse(weatherData, timeRef) {
        const temp = Math.round(weatherData.temperature);
        const condition = weatherData.condition.toLowerCase();
        const city = weatherData.location;
        
        let timePrefix = '';
        switch (timeRef) {
            case 'tomorrow':
                timePrefix = 'Tomorrow, ';
                break;
            case 'tonight':
                timePrefix = 'Tonight, ';
                break;
            case 'morning':
                timePrefix = 'This morning, ';
                break;
            case 'afternoon':
                timePrefix = 'This afternoon, ';
                break;
            case 'today':
                timePrefix = 'Today, ';
                break;
            default:
                timePrefix = 'Currently, ';
        }

        return `${timePrefix}in ${city}, it's ${temp} degrees with ${condition}.`;
    }

    updateWeatherUI(weatherData) {
        // Update the current city in the app
        if (window.themeManager) {
            // Update session or local storage
            sessionStorage.setItem('currentCity', weatherData.location);
        }

        // Trigger a page refresh or update the weather display
        // This could be enhanced to update the UI without a full refresh
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    }

    updateUI() {
        // Update voice assistant button appearance
        const voiceBtn = document.getElementById('voice-assistant-btn');
        if (voiceBtn) {
            if (this.isListening) {
                voiceBtn.classList.add('listening');
                voiceBtn.innerHTML = '<i data-feather="mic-off"></i>';
            } else if (this.isSpeaking) {
                voiceBtn.classList.add('speaking');
                voiceBtn.innerHTML = '<i data-feather="volume-2"></i>';
            } else {
                voiceBtn.classList.remove('listening', 'speaking');
                voiceBtn.innerHTML = '<i data-feather="mic"></i>';
            }
            
            // Re-render feather icons
            if (typeof feather !== 'undefined') {
                feather.replace();
            }
        }
    }

    // Public method to set current city
    setCurrentCity(city) {
        this.currentCity = city;
    }

    // Public method to get current status
    getStatus() {
        return {
            isListening: this.isListening,
            isSpeaking: this.isSpeaking,
            currentCity: this.currentCity
        };
    }

    mapCityName(city) {
        // Map common nicknames and variations to standard city names
        const cityMappings = {
            'vizag': 'visakhapatnam',
            'vishakapatnam': 'visakhapatnam',
            'vishakhapatnam': 'visakhapatnam',
            'bombay': 'mumbai',
            'calcutta': 'kolkata',
            'madras': 'chennai',
            'bangalore': 'bengaluru',
            'bangaluru': 'bengaluru',
            'delhi': 'new delhi',
            'new delhi': 'new delhi',
            'old delhi': 'delhi',
            'banglore': 'bengaluru',
            'bengalore': 'bengaluru',
            'hyd': 'hyderabad',
            'hydrabad': 'hyderabad',
            'hydrabad': 'hyderabad',
            'pune': 'pune',
            'poona': 'pune',
            'ahmedabad': 'ahmedabad',
            'amadavad': 'ahmedabad',
            'surat': 'surat',
            'jaipur': 'jaipur',
            'lucknow': 'lucknow',
            'kanpur': 'kanpur',
            'nagpur': 'nagpur',
            'indore': 'indore',
            'thane': 'thane',
            'bhopal': 'bhopal',
            'visakhapatnam': 'visakhapatnam',
            'vijayawada': 'vijayawada',
            'guntur': 'guntur',
            'srikakulam': 'srikakulam',
            'krishna': 'vijayawada', // Krishna district, major city is Vijayawada
            'krishna lanka': 'vijayawada', // Specific area in Vijayawada
            'goa': 'goa',
            'panaji': 'panaji',
            'panjim': 'panaji',
            'margao': 'margao',
            'vasco': 'vasco da gama',
            'vasco da gama': 'vasco da gama',
            'tokyo': 'tokyo',
            'london': 'london',
            'paris': 'paris',
            'new york': 'new york',
            'sydney': 'sydney',
            'mumbai': 'mumbai',
            'kolkata': 'kolkata',
            'chennai': 'chennai',
            'bengaluru': 'bengaluru',
            'hyderabad': 'hyderabad'
        };

        const cityLower = city.toLowerCase().trim();
        
        // Check if we have a direct mapping
        if (cityMappings[cityLower]) {
            return cityMappings[cityLower];
        }

        // Check if any part of the city name matches
        for (const [nickname, standardName] of Object.entries(cityMappings)) {
            if (cityLower.includes(nickname) || nickname.includes(cityLower)) {
                return standardName;
            }
        }

        // If no mapping found, return the original city name
        return city;
    }
}

// Initialize voice assistant when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.weatherVoiceAssistant = new WeatherVoiceAssistant();
    
    // Set the current city from the page if available
    const cityElement = document.querySelector('.current-city, .city-name, h1, .weather-location');
    if (cityElement) {
        const currentCity = cityElement.textContent.trim();
        if (currentCity && currentCity !== 'Weather') {
            window.weatherVoiceAssistant.setCurrentCity(currentCity);
            console.log('Set current city to:', currentCity);
        }
    }
});

// Global function to start voice assistant
function startVoiceAssistant() {
    if (window.weatherVoiceAssistant) {
        window.weatherVoiceAssistant.startListening();
    }
}

// Global function to test voice recognition
function testVoiceRecognition() {
    if (window.weatherVoiceAssistant) {
        console.log('Starting voice recognition test...');
        window.weatherVoiceAssistant.startListening();
    } else {
        console.error('Voice assistant not initialized');
    }
}

// Global function to test city extraction
function testCityExtraction(testTranscript) {
    if (window.weatherVoiceAssistant) {
        console.log('=== TESTING CITY EXTRACTION ===');
        console.log('Test transcript:', testTranscript);
        const extractedCity = window.weatherVoiceAssistant.extractCity(testTranscript);
        console.log('Extracted city:', extractedCity);
        return extractedCity;
    } else {
        console.error('Voice assistant not initialized');
        return null;
    }
}

// Test cases for city extraction
function runCityExtractionTests() {
    const testCases = [
        // Basic cases
        'what is the weather in tokyo',
        'what\'s the weather in london',
        'how is the weather in new york',
        'tell me the weather in paris',
        'weather in sydney',
        'forecast for mumbai',
        'temperature in berlin',
        'is the weather in tokyo',
        'the weather in london',
        'tokyo weather',
        'london forecast',
        'new york temperature',
        'paris',
        'sydney',
        'mumbai',
        'berlin',
        
        // Indian cities
        'what is the weather in srikakulam',
        'weather in guntur',
        'forecast for hyderabad',
        'temperature in bangalore',
        'weather in vizag',
        'forecast for vijayawada',
        'weather in krishna lanka',
        'temperature in goa',
        'weather in delhi',
        'forecast for mumbai',
        'weather in chennai',
        'temperature in kolkata',
        
        // Problematic cases that should be fixed
        'listening weather forecast of vijayawada',
        'listening',
        'krishna lanka',
        'vizag',
        'is the weather in tokyo',
        'ecast of srikakulam',
        'vision peta',
        'srikakula',
        'what is the weather in',
        'weather in',
        'forecast for',
        'temperature in'
    ];

    console.log('=== RUNNING CITY EXTRACTION TESTS ===');
    testCases.forEach(testCase => {
        testCityExtraction(testCase);
    });
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WeatherVoiceAssistant;
} 