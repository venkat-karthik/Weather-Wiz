"""
Affiliate Products Database - Simplified for Vercel
"""

# Your Amazon Affiliate Tag
AFFILIATE_TAG = "your-affiliate-tag-20"  # Replace with your actual affiliate tag

# Simplified Product Database
AFFILIATE_PRODUCTS = {
    "casual": {
        "hot": {
            "tops": [
                {
                    "name": "Comfortable Cotton T-Shirt",
                    "brand": "Generic",
                    "price": "$15.99",
                    "amazon_asin": "B077ZQZX8Q",
                    "image": "https://via.placeholder.com/300x300?text=T-Shirt",
                    "rating": 4.5,
                    "description": "Comfortable 100% cotton t-shirt perfect for hot weather",
                    "features": ["100% Cotton", "Tagless", "Pre-shrunk", "Machine Washable"]
                }
            ],
            "bottoms": [
                {
                    "name": "Casual Shorts",
                    "brand": "Generic",
                    "price": "$25.99",
                    "amazon_asin": "B07EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Shorts",
                    "rating": 4.3,
                    "description": "Comfortable casual shorts for hot weather",
                    "features": ["Quick-Dry", "Lightweight", "Comfortable Fit"]
                }
            ],
            "footwear": [
                {
                    "name": "Comfortable Sneakers",
                    "brand": "Generic",
                    "price": "$49.99",
                    "amazon_asin": "B08EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Sneakers",
                    "rating": 4.4,
                    "description": "Comfortable sneakers for everyday wear",
                    "features": ["Breathable", "Comfortable", "Durable"]
                }
            ],
            "accessories": [
                {
                    "name": "Sun Hat",
                    "brand": "Generic",
                    "price": "$19.99",
                    "amazon_asin": "B01EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Hat",
                    "rating": 4.2,
                    "description": "Protective sun hat for hot weather",
                    "features": ["UV Protection", "Adjustable", "Lightweight"]
                }
            ]
        },
        "warm": {
            "tops": [
                {
                    "name": "Casual Button Shirt",
                    "brand": "Generic",
                    "price": "$35.99",
                    "amazon_asin": "B09EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Shirt",
                    "rating": 4.2,
                    "description": "Comfortable button-down shirt",
                    "features": ["Cotton Blend", "Wrinkle Resistant", "Comfortable Fit"]
                }
            ],
            "bottoms": [
                {
                    "name": "Casual Pants",
                    "brand": "Generic",
                    "price": "$45.99",
                    "amazon_asin": "B00EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Pants",
                    "rating": 4.5,
                    "description": "Comfortable casual pants",
                    "features": ["Stretch Fabric", "Machine Washable", "Regular Fit"]
                }
            ],
            "footwear": [
                {
                    "name": "Walking Shoes",
                    "brand": "Generic",
                    "price": "$65.99",
                    "amazon_asin": "B09EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Shoes",
                    "rating": 4.6,
                    "description": "Comfortable walking shoes",
                    "features": ["Cushioned", "Breathable", "Durable"]
                }
            ],
            "accessories": []
        },
        "cool": {
            "tops": [
                {
                    "name": "Light Sweater",
                    "brand": "Generic",
                    "price": "$55.99",
                    "amazon_asin": "B01EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Sweater",
                    "rating": 4.4,
                    "description": "Comfortable light sweater for cool weather",
                    "features": ["Soft Material", "Machine Washable", "Comfortable Fit"]
                }
            ],
            "bottoms": [
                {
                    "name": "Warm Pants",
                    "brand": "Generic",
                    "price": "$65.99",
                    "amazon_asin": "B08EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Pants",
                    "rating": 4.5,
                    "description": "Warm pants for cool weather",
                    "features": ["Insulated", "Comfortable", "Durable"]
                }
            ],
            "footwear": [
                {
                    "name": "Warm Boots",
                    "brand": "Generic",
                    "price": "$85.99",
                    "amazon_asin": "B00EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Boots",
                    "rating": 4.6,
                    "description": "Warm boots for cool weather",
                    "features": ["Insulated", "Waterproof", "Comfortable"]
                }
            ],
            "accessories": [
                {
                    "name": "Light Scarf",
                    "brand": "Generic",
                    "price": "$25.99",
                    "amazon_asin": "B07EXAMPLE",
                    "image": "https://via.placeholder.com/300x300?text=Scarf",
                    "rating": 4.3,
                    "description": "Light scarf for cool weather",
                    "features": ["Soft", "Warm", "Stylish"]
                }
            ]
        }
    }
}

def generate_affiliate_url(asin, affiliate_tag=AFFILIATE_TAG):
    """Generate Amazon affiliate URL from ASIN"""
    return f"https://www.amazon.com/dp/{asin}?tag={affiliate_tag}&linkCode=as2&creative=9325&creativeASIN={asin}"

def get_products_by_weather(style, temperature_category):
    """Get products for specific style and temperature"""
    try:
        products = AFFILIATE_PRODUCTS.get(style, {}).get(temperature_category, {})
        
        # Add affiliate URLs to products
        for category in products:
            for product in products[category]:
                if 'amazon_asin' in product:
                    product['affiliateUrl'] = generate_affiliate_url(product['amazon_asin'])
                else:
                    product['affiliateUrl'] = '#'
        
        return products
    except Exception as e:
        print(f"Error getting products: {e}")
        return {}