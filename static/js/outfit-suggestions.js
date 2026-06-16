// AI Outfit Suggestions System with Amazon Affiliate Integration
class OutfitSuggestions {
    constructor() {
        this.userPreferences = this.loadPreferences();
        this.weatherConditions = {};
        this.affiliateTag = 'your-affiliate-tag'; // Replace with your Amazon affiliate tag
        this.outfitDatabase = this.initializeAffiliateDatabase();
    }

    // Load user preferences from localStorage
    loadPreferences() {
        const saved = localStorage.getItem('outfitPreferences');
        return saved ? JSON.parse(saved) : {
            style: 'casual', // casual, formal, sporty, trendy
            comfort: 'medium', // low, medium, high
            layers: 'medium', // light, medium, heavy
            colors: ['blue', 'black', 'white', 'gray'], // preferred colors
            accessories: true,
            footwear: 'comfortable',
            budget: 'medium' // low, medium, high
        };
    }

    // Save user preferences to localStorage
    savePreferences() {
        localStorage.setItem('outfitPreferences', JSON.stringify(this.userPreferences));
    }

    // Initialize affiliate database with real Amazon products
    initializeAffiliateDatabase() {
        // This will be populated from the server-side affiliate_products.py
        // For now, return a basic structure that matches the server response
        return {
            temperature: {
                hot: { tops: [], bottoms: [], footwear: [], accessories: [] },
                warm: { tops: [], bottoms: [], footwear: [], accessories: [] },
                mild: { tops: [], bottoms: [], footwear: [], accessories: [] },
                cool: { tops: [], bottoms: [], footwear: [], accessories: [] },
                cold: { tops: [], bottoms: [], footwear: [], accessories: [] },
                freezing: { tops: [], bottoms: [], footwear: [], accessories: [] }
            }
        };
    }

    // Fetch products from server
    async fetchProducts(style, temperatureCategory) {
        try {
            const response = await fetch('/api/affiliate-products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    style: style,
                    temperature_category: temperatureCategory
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch products');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching products:', error);
            return this.getFallbackProducts(temperatureCategory);
        }
    }

    // Fallback products if server request fails
    getFallbackProducts(temperatureCategory) {
        const fallbackProducts = {
            hot: {
                tops: [{
                    name: 'Cotton T-Shirt',
                    brand: 'Generic',
                    price: '$15.99',
                    affiliateUrl: '#',
                    image: 'https://via.placeholder.com/300x300?text=Cotton+T-Shirt',
                    rating: 4.0,
                    description: 'Comfortable cotton t-shirt for hot weather',
                    features: ['100% Cotton', 'Breathable', 'Machine Washable']
                }],
                bottoms: [{
                    name: 'Cotton Shorts',
                    brand: 'Generic',
                    price: '$25.99',
                    affiliateUrl: '#',
                    image: 'https://via.placeholder.com/300x300?text=Cotton+Shorts',
                    rating: 4.2,
                    description: 'Lightweight shorts for warm weather',
                    features: ['Quick-Dry', 'Comfortable Fit', 'Multiple Pockets']
                }],
                footwear: [{
                    name: 'Canvas Sneakers',
                    brand: 'Generic',
                    price: '$45.99',
                    affiliateUrl: '#',
                    image: 'https://via.placeholder.com/300x300?text=Canvas+Sneakers',
                    rating: 4.1,
                    description: 'Breathable canvas sneakers',
                    features: ['Canvas Upper', 'Rubber Sole', 'Comfortable']
                }],
                accessories: [{
                    name: 'Sunglasses',
                    brand: 'Generic',
                    price: '$29.99',
                    affiliateUrl: '#',
                    image: 'https://via.placeholder.com/300x300?text=Sunglasses',
                    rating: 4.3,
                    description: 'UV protection sunglasses',
                    features: ['UV Protection', 'Durable Frame', 'Stylish']
                }]
            }
            // Add other temperature categories as needed
        };
        
        return fallbackProducts[temperatureCategory] || fallbackProducts.hot;
    }

    // Generate Amazon affiliate URL
    generateAffiliateUrl(productId, productName) {
        // This would be replaced with actual Amazon product URLs
        const baseUrl = 'https://www.amazon.com/dp/';
        const affiliateParams = `?tag=${this.affiliateTag}&linkCode=as2&creative=9325&creativeASIN=${productId}`;
        return `${baseUrl}${productId}${affiliateParams}`;
    }

    // Get temperature category
    getTemperatureCategory(temp) {
        if (temp >= 25) return 'hot';
        if (temp >= 18) return 'warm';
        if (temp >= 10) return 'mild';
        if (temp >= 5) return 'cool';
        if (temp >= 0) return 'cold';
        return 'freezing';
    }

    // Get weather condition category
    getWeatherCondition(description) {
        const desc = description.toLowerCase();
        if (desc.includes('rain') || desc.includes('drizzle')) return 'rainy';
        if (desc.includes('snow') || desc.includes('sleet')) return 'snowy';
        if (desc.includes('wind') || desc.includes('breeze')) return 'windy';
        if (desc.includes('fog') || desc.includes('mist')) return 'foggy';
        if (desc.includes('cloud') || desc.includes('overcast')) return 'cloudy';
        if (desc.includes('clear') || desc.includes('sun')) return 'sunny';
        return 'cloudy'; // default
    }

    async generateSuggestion(weatherData, style = null) {
        const temp = weatherData.temperature;
        const condition = weatherData.description;
        const humidity = weatherData.humidity;
        const windSpeed = weatherData.windSpeed;
        
        const tempCategory = this.getTemperatureCategory(temp);
        const weatherCategory = this.getWeatherCondition(condition);
        
        // Respect style parameter, fallback to user preferences or 'casual'
        const activeStyle = style || this.userPreferences.style || 'casual';
        
        // Fetch products from server
        const products = await this.fetchProducts(activeStyle, tempCategory);
        
        // Select products based on preferences
        const suggestion = {
            temperature: temp,
            condition: condition,
            category: tempCategory,
            style: style,
            outfit: {
                top: this.selectProduct(products.tops || []),
                bottom: this.selectProduct(products.bottoms || []),
                footwear: this.selectProduct(products.footwear || []),
                accessories: this.selectAccessories(products.accessories || [])
            },
            reasoning: this.generateReasoning(temp, condition, humidity, windSpeed),
            tips: this.generateTips(temp, condition, humidity, windSpeed),
            totalPrice: 0
        };
        
        // Calculate total price
        suggestion.totalPrice = this.calculateTotalPrice(suggestion.outfit);
        
        return suggestion;
    }

    // Select product based on preferences and budget
    selectProduct(products) {
        if (!products || products.length === 0) return null;
        
        // Filter by budget if specified
        let filteredProducts = products;
        if (this.userPreferences.budget === 'low') {
            filteredProducts = products.filter(p => parseFloat(p.price.replace('$', '')) < 50);
        } else if (this.userPreferences.budget === 'high') {
            filteredProducts = products.filter(p => parseFloat(p.price.replace('$', '')) > 100);
        }
        
        if (filteredProducts.length === 0) filteredProducts = products;
        
        // Select highest rated product within budget
        return filteredProducts.sort((a, b) => b.rating - a.rating)[0];
    }

    // Select accessories based on weather and preferences
    selectAccessories(accessories) {
        if (!accessories || accessories.length === 0) return [];
        
        if (!this.userPreferences.accessories) return [];
        
        // Select up to 2 accessories
        return accessories.slice(0, 2);
    }

    // Calculate total price of outfit
    calculateTotalPrice(outfit) {
        let total = 0;
        
        if (outfit.top) total += parseFloat(outfit.top.price.replace('$', ''));
        if (outfit.bottom) total += parseFloat(outfit.bottom.price.replace('$', ''));
        if (outfit.footwear) total += parseFloat(outfit.footwear.price.replace('$', ''));
        
        outfit.accessories.forEach(acc => {
            total += parseFloat(acc.price.replace('$', ''));
        });
        
        return total.toFixed(2);
    }

    // Generate reasoning for the suggestion
    generateReasoning(temp, condition, humidity, windSpeed) {
        const reasons = [];
        
        // Temperature reasoning
        if (temp >= 25) {
            reasons.push(`With temperatures at ${temp}°C, we've selected lightweight, breathable materials to keep you cool and comfortable.`);
        } else if (temp >= 15) {
            reasons.push(`At ${temp}°C, these pieces provide the perfect balance of comfort and style for mild weather.`);
        } else if (temp >= 5) {
            reasons.push(`For ${temp}°C weather, we've chosen insulated items that provide warmth without bulk.`);
        } else {
            reasons.push(`In ${temp}°C conditions, these cold-weather essentials offer maximum protection and warmth.`);
        }
        
        // Weather condition reasoning
        if (condition.toLowerCase().includes('rain')) {
            reasons.push('Water-resistant materials are prioritized to keep you dry.');
        } else if (condition.toLowerCase().includes('sun')) {
            reasons.push('UV protection and breathable fabrics are essential for sunny conditions.');
        } else if (condition.toLowerCase().includes('wind')) {
            reasons.push('Wind-resistant outer layers help maintain comfort in breezy conditions.');
        }
        
        return reasons.join(' ');
    }

    // Generate additional tips
    generateTips(temp, condition, humidity, windSpeed) {
        const tips = [];
        
        // Temperature tips
        if (temp >= 25) {
            tips.push('Choose light colors to reflect heat and stay hydrated throughout the day.');
        } else if (temp <= 0) {
            tips.push('Layer up and ensure all extremities are covered to prevent cold-related injuries.');
        }
        
        // Weather tips
        if (condition.toLowerCase().includes('rain')) {
            tips.push('Consider adding a waterproof jacket and umbrella to your outfit.');
        } else if (condition.toLowerCase().includes('sun')) {
            tips.push('Don\'t forget sunscreen and consider a hat for additional sun protection.');
        }
        
        // General tips
        tips.push('All recommended items are available through our affiliate partners with fast shipping.');
        tips.push('Check size guides before purchasing to ensure the best fit.');
        
        return tips;
    }

    // Update user preferences
    updatePreferences(newPreferences) {
        this.userPreferences = { ...this.userPreferences, ...newPreferences };
        this.savePreferences();
    }

    // Get current preferences
    getPreferences() {
        return this.userPreferences;
    }

    formatSuggestion(suggestion) {
        const topName = suggestion.outfit.top ? `${suggestion.outfit.top.name} by ${suggestion.outfit.top.brand} (${suggestion.outfit.top.price})` : "None";
        const bottomName = suggestion.outfit.bottom ? `${suggestion.outfit.bottom.name} by ${suggestion.outfit.bottom.brand} (${suggestion.outfit.bottom.price})` : "None";
        const footwearName = suggestion.outfit.footwear ? `${suggestion.outfit.footwear.name} by ${suggestion.outfit.footwear.brand} (${suggestion.outfit.footwear.price})` : "None";
        
        const accessoryNames = (suggestion.outfit.accessories && suggestion.outfit.accessories.length > 0)
            ? suggestion.outfit.accessories.map(acc => `${acc.name} (${acc.price})`).join(', ')
            : "None";

        return {
            summary: `Complete outfit for ${suggestion.temperature}°C, ${suggestion.condition}`,
            totalPrice: `$${suggestion.totalPrice}`,
            items: {
                top: suggestion.outfit.top,
                bottom: suggestion.outfit.bottom,
                footwear: suggestion.outfit.footwear,
                accessories: suggestion.outfit.accessories
            },
            details: {
                top: topName,
                bottom: bottomName,
                footwear: footwearName,
                accessories: accessoryNames,
                layers: suggestion.category === 'freezing' || suggestion.category === 'cold' ? 'Heavy Layers (Thermal + Fleece + Outerwear)' : (suggestion.category === 'cool' || suggestion.category === 'mild' ? 'Light Layers (Sweater/Jacket)' : 'No layering needed')
            },
            reasoning: suggestion.reasoning,
            tips: suggestion.tips
        };
    }
}

// Global instance
const outfitSuggestions = new OutfitSuggestions();

// Global function to get outfit suggestion
async function getOutfitSuggestion(weatherData) {
    if (outfitSuggestions) {
        try {
            const suggestion = await outfitSuggestions.generateSuggestion(weatherData);
            return outfitSuggestions.formatSuggestion(suggestion);
        } catch (error) {
            console.error("Error in getOutfitSuggestion:", error);
            return null;
        }
    }
    return null;
}

// Global function to update preferences
function updateOutfitPreferences(preferences) {
    if (outfitSuggestions) {
        outfitSuggestions.updatePreferences(preferences);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OutfitSuggestions;
} 