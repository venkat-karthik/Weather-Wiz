"""
Affiliate Products Database
Add your Amazon affiliate links here
"""

# Your Amazon Affiliate Tag
AFFILIATE_TAG = "your-affiliate-tag-20"  # Replace with your actual affiliate tag

# Product Database with Real Amazon Affiliate Links
AFFILIATE_PRODUCTS = {
    "casual": {
        "hot": {
            "tops": [
                {
                    "name": "Hanes Men's Cotton T-Shirt",
                    "brand": "Hanes",
                    "price": "$12.99",
                    "amazon_asin": "B077ZQZX8Q",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.5,
                    "description": "Comfortable 100% cotton t-shirt perfect for hot weather",
                    "features": ["100% Cotton", "Tagless", "Pre-shrunk", "Machine Washable"]
                },
                {
                    "name": "Uniqlo Airism T-Shirt",
                    "brand": "Uniqlo",
                    "price": "$14.90",
                    "amazon_asin": "B08EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.3,
                    "description": "Ultra-lightweight and quick-drying t-shirt",
                    "features": ["Quick-Dry", "Anti-Odor", "UV Protection", "Smooth Feel"]
                }
            ],
            "bottoms": [
                {
                    "name": "Patagonia Baggies Shorts 5\"",
                    "brand": "Patagonia",
                    "price": "$55.00",
                    "amazon_asin": "B07EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.6,
                    "description": "Versatile shorts made from recycled materials",
                    "features": ["Quick-Dry", "DWR Finish", "Recycled Nylon", "5\" Inseam"]
                }
            ],
            "footwear": [
                {
                    "name": "Allbirds Tree Runners",
                    "brand": "Allbirds",
                    "price": "$98.00",
                    "amazon_asin": "B08EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.4,
                    "description": "Sustainable sneakers made from eucalyptus tree fiber",
                    "features": ["Eucalyptus Fiber", "Machine Washable", "Carbon Neutral", "Breathable"]
                }
            ],
            "accessories": [
                {
                    "name": "Ray-Ban Wayfarer Sunglasses",
                    "brand": "Ray-Ban",
                    "price": "$154.00",
                    "amazon_asin": "B001EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.7,
                    "description": "Classic sunglasses with 100% UV protection",
                    "features": ["100% UV Protection", "Polarized", "Acetate Frame", "Crystal Lenses"]
                }
            ]
        },
        "warm": {
            "tops": [
                {
                    "name": "J.Crew Flex Casual Shirt",
                    "brand": "J.Crew",
                    "price": "$49.50",
                    "amazon_asin": "B09EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.2,
                    "description": "Comfortable button-down shirt with stretch",
                    "features": ["Stretch Cotton", "Wrinkle Resistant", "Tailored Fit", "Easy Care"]
                }
            ],
            "bottoms": [
                {
                    "name": "Levi's 511 Slim Jeans",
                    "brand": "Levi's",
                    "price": "$59.99",
                    "amazon_asin": "B00EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.5,
                    "description": "Classic slim-fit jeans with stretch",
                    "features": ["Stretch Denim", "Slim Fit", "5-Pocket Style", "Machine Washable"]
                }
            ],
            "footwear": [
                {
                    "name": "Adidas Ultraboost 22",
                    "brand": "Adidas",
                    "price": "$190.00",
                    "amazon_asin": "B09EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.6,
                    "description": "Premium running shoes with boost technology",
                    "features": ["Boost Midsole", "Primeknit Upper", "Continental Rubber", "Energy Return"]
                }
            ],
            "accessories": []
        },
        "mild": {
            "tops": [
                {
                    "name": "Uniqlo Merino Wool Sweater",
                    "brand": "Uniqlo",
                    "price": "$39.90",
                    "amazon_asin": "B08EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.4,
                    "description": "Soft merino wool crew neck sweater",
                    "features": ["100% Merino Wool", "Machine Washable", "Odor Resistant", "Temperature Regulating"]
                }
            ],
            "bottoms": [
                {
                    "name": "Dockers Alpha Khaki Chinos",
                    "brand": "Dockers",
                    "price": "$39.99",
                    "amazon_asin": "B01EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.1,
                    "description": "Versatile chino pants for smart casual looks",
                    "features": ["Cotton Twill", "Tapered Fit", "Wrinkle Resistant", "Stain Defender"]
                }
            ],
            "footwear": [
                {
                    "name": "Clarks Desert Boot",
                    "brand": "Clarks",
                    "price": "$130.00",
                    "amazon_asin": "B00EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.5,
                    "description": "Classic desert boot in premium suede",
                    "features": ["Suede Upper", "Crepe Sole", "Lace-Up", "Cushioned Footbed"]
                }
            ],
            "accessories": [
                {
                    "name": "Acne Studios Wool Scarf",
                    "brand": "Acne Studios",
                    "price": "$180.00",
                    "amazon_asin": "B07EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.8,
                    "description": "Luxurious wool scarf in classic design",
                    "features": ["100% Wool", "Oversized", "Fringed Edges", "Soft Texture"]
                }
            ]
        },
        "cool": {
            "tops": [
                {
                    "name": "Patagonia Better Sweater Fleece",
                    "brand": "Patagonia",
                    "price": "$99.00",
                    "amazon_asin": "B01EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.7,
                    "description": "Warm fleece jacket made from recycled polyester",
                    "features": ["Recycled Polyester", "Full-Zip", "Stand-Up Collar", "Fair Trade Certified"]
                }
            ],
            "bottoms": [
                {
                    "name": "Smartwool Merino Base Layer",
                    "brand": "Smartwool",
                    "price": "$75.00",
                    "amazon_asin": "B08EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.5,
                    "description": "Merino wool base layer for temperature regulation",
                    "features": ["Merino Wool", "Odor Resistant", "Temperature Regulating", "Moisture Wicking"]
                }
            ],
            "footwear": [
                {
                    "name": "Timberland 6-Inch Premium Boot",
                    "brand": "Timberland",
                    "price": "$190.00",
                    "amazon_asin": "B00EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.6,
                    "description": "Waterproof leather boots for all conditions",
                    "features": ["Waterproof", "Premium Leather", "Padded Collar", "Rust-Proof Hardware"]
                }
            ],
            "accessories": [
                {
                    "name": "The North Face Etip Gloves",
                    "brand": "The North Face",
                    "price": "$35.00",
                    "amazon_asin": "B01EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.3,
                    "description": "Touchscreen compatible fleece gloves",
                    "features": ["Touchscreen Compatible", "Fleece Lining", "Silicone Grip", "Elastic Wrist"]
                }
            ]
        },
        "cold": {
            "tops": [
                {
                    "name": "Canada Goose Expedition Parka",
                    "brand": "Canada Goose",
                    "price": "$1,150.00",
                    "amazon_asin": "B07EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.8,
                    "description": "Extreme cold weather parka with down insulation",
                    "features": ["625 Fill Down", "Arctic Tech Fabric", "Coyote Fur Trim", "Temperature Rated"]
                }
            ],
            "bottoms": [
                {
                    "name": "Arc'teryx Atom LT Vest",
                    "brand": "Arc'teryx",
                    "price": "$259.00",
                    "amazon_asin": "B08EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.7,
                    "description": "Insulated vest for core warmth",
                    "features": ["Coreloft Insulation", "Wind Resistant", "Packable", "Trim Fit"]
                }
            ],
            "footwear": [
                {
                    "name": "Sorel Caribou Boot",
                    "brand": "Sorel",
                    "price": "$160.00",
                    "amazon_asin": "B00EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.5,
                    "description": "Waterproof winter boots rated to -40°F",
                    "features": ["Waterproof", "Removable Liner", "Seam-Sealed", "Temperature Rated"]
                }
            ],
            "accessories": [
                {
                    "name": "Carhartt Acrylic Watch Hat",
                    "brand": "Carhartt",
                    "price": "$16.99",
                    "amazon_asin": "B00EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.6,
                    "description": "Warm acrylic knit hat",
                    "features": ["Acrylic Knit", "Stretchable", "Carhartt Label", "One Size"]
                }
            ]
        },
        "freezing": {
            "tops": [
                {
                    "name": "Canada Goose Snow Mantra Parka",
                    "brand": "Canada Goose",
                    "price": "$1,695.00",
                    "amazon_asin": "B08EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.9,
                    "description": "Ultimate extreme cold weather protection",
                    "features": ["625 Fill Down", "TEI Rating 5", "Recco Reflector", "Removable Hood"]
                }
            ],
            "bottoms": [
                {
                    "name": "Arc'teryx Fission SV Pant",
                    "brand": "Arc'teryx",
                    "price": "$525.00",
                    "amazon_asin": "B09EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.8,
                    "description": "Insulated pants for extreme conditions",
                    "features": ["Gore-Tex Pro", "Coreloft Insulation", "Reinforced", "Articulated Patterning"]
                }
            ],
            "footwear": [
                {
                    "name": "Baffin Impact Boot",
                    "brand": "Baffin",
                    "price": "$280.00",
                    "amazon_asin": "B01EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.7,
                    "description": "Extreme cold weather boots rated to -148°F",
                    "features": ["Rated to -148°F", "Waterproof", "Removable Liner", "Vibram Sole"]
                }
            ],
            "accessories": [
                {
                    "name": "Outdoor Research Alti Mitts",
                    "brand": "Outdoor Research",
                    "price": "$89.00",
                    "amazon_asin": "B07EXAMPLE",  # Replace with actual ASIN
                    "image": "https://m.media-amazon.com/images/I/placeholder.jpg",
                    "rating": 4.6,
                    "description": "Insulated mitts for extreme cold",
                    "features": ["Gore-Tex", "PrimaLoft Insulation", "Removable Liner", "Wrist Leash"]
                }
            ]
        }
    }
    # Add more styles (formal, sporty, trendy) following the same structure
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
                    product['affiliateUrl'] = '#'  # Fallback for products without ASIN
        
        return products
    except Exception as e:
        print(f"Error getting products: {e}")
        return {}

def add_product(style, temperature, category, product_data):
    """Add a new product to the database"""
    if style not in AFFILIATE_PRODUCTS:
        AFFILIATE_PRODUCTS[style] = {}
    if temperature not in AFFILIATE_PRODUCTS[style]:
        AFFILIATE_PRODUCTS[style][temperature] = {}
    if category not in AFFILIATE_PRODUCTS[style][temperature]:
        AFFILIATE_PRODUCTS[style][temperature][category] = []
    
    AFFILIATE_PRODUCTS[style][temperature][category].append(product_data)

# Example of how to add new products:
"""
add_product('casual', 'hot', 'tops', {
    "name": "New Product Name",
    "brand": "Brand Name",
    "price": "$XX.XX",
    "amazon_asin": "B0XXXXXXXX",  # Get this from Amazon product URL
    "image": "https://m.media-amazon.com/images/I/product-image.jpg",
    "rating": 4.5,
    "description": "Product description",
    "features": ["Feature 1", "Feature 2", "Feature 3"]
})
"""