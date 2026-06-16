"""
Affiliate Products Database - Expanded and Premium
Contains full recommendations for all styles (casual, formal, sporty, trendy)
and temperature categories (hot, warm, mild, cool, cold, freezing).
"""

AFFILIATE_TAG = "weatherwiz-20"  # Dynamic affiliate tag

AFFILIATE_PRODUCTS = {
    "casual": {
        "hot": {
            "tops": [
                {
                    "name": "Breathable Cotton Crewneck Tee",
                    "brand": "Everlane",
                    "price": "$18.00",
                    "amazon_asin": "B077ZQZX8Q",
                    "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
                    "rating": 4.6,
                    "description": "Premium 100% organic cotton tee. Lightweight, soft, and perfect for hot days.",
                    "features": ["100% Organic Cotton", "Tagless Neck", "Pre-shrunk", "Highly Breathable"]
                }
            ],
            "bottoms": [
                {
                    "name": "Lightweight Linen Blend Shorts",
                    "brand": "Club Monaco",
                    "price": "$29.50",
                    "amazon_asin": "B07EXAMPLE1",
                    "image": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500",
                    "rating": 4.4,
                    "description": "Easy-wearing linen-blend shorts with an elastic drawstring waist for ultimate hot-weather comfort.",
                    "features": ["Linen-Cotton Blend", "Drawstring Waist", "Relaxed Fit", "Deep Side Pockets"]
                }
            ],
            "footwear": [
                {
                    "name": "Minimalist Leather Strap Sandals",
                    "brand": "Birkenstock",
                    "price": "$59.99",
                    "amazon_asin": "B08EXAMPLE1",
                    "image": "https://images.unsplash.com/photo-1603487226258-414a77935767?w=500",
                    "rating": 4.7,
                    "description": "Classic strap sandals with a contoured cork footbed that molds to your feet.",
                    "features": ["Genuine Leather", "Cork Footbed", "Dual Adjustable Straps", "Shock-Absorbing Sole"]
                }
            ],
            "accessories": [
                {
                    "name": "Polarized Wayfarer Sunglasses",
                    "brand": "Ray-Ban",
                    "price": "$35.00",
                    "amazon_asin": "B01EXAMPLE1",
                    "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500",
                    "rating": 4.5,
                    "description": "Timeless polarized sunglasses offering complete UV400 protection.",
                    "features": ["Polarized Lenses", "UV400 Protection", "Impact Resistant Frame", "Classic Unisex Design"]
                }
            ]
        },
        "warm": {
            "tops": [
                {
                    "name": "Relaxed Fit Cotton Linen Shirt",
                    "brand": "J.Crew",
                    "price": "$38.50",
                    "amazon_asin": "B09EXAMPLE1",
                    "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500",
                    "rating": 4.3,
                    "description": "An airy linen-cotton shirt with a relaxed, modern fit suitable for warm breezy days.",
                    "features": ["Air-Woven Linen", "Button-Down Collar", "Chest Pocket", "Adjustable Cuffs"]
                }
            ],
            "bottoms": [
                {
                    "name": "Stretch Cotton Chino Pants",
                    "brand": "Bonobos",
                    "price": "$48.00",
                    "amazon_asin": "B00EXAMPLE1",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.5,
                    "description": "Slim, versatile chinos made with a hint of stretch for active all-day comfort.",
                    "features": ["98% Cotton, 2% Elastane", "Scratch-Resistant Zip Fly", "Breathable Twill", "Wrinkle-Resistant"]
                }
            ],
            "footwear": [
                {
                    "name": "Classic Low-Top Canvas Sneakers",
                    "brand": "Converse",
                    "price": "$45.00",
                    "amazon_asin": "B09EXAMPLE2",
                    "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500",
                    "rating": 4.6,
                    "description": "Timeless canvas sneakers that go perfectly with casual chinos or shorts.",
                    "features": ["Durable Canvas Upper", "Vulcanized Rubber Sole", "Medial Eyelets for Airflow", "Ortholite Cushioning"]
                }
            ],
            "accessories": [
                {
                    "name": "Woven Cotton Web Belt",
                    "brand": "Columbia",
                    "price": "$15.99",
                    "amazon_asin": "B07EXAMPLE2",
                    "image": "https://images.unsplash.com/photo-1624222247344-550fb8ec5522?w=500",
                    "rating": 4.2,
                    "description": "An adjustable woven utility belt with a metal clamp buckle.",
                    "features": ["100% Cotton Fiber", "Durable Metal Buckle", "Fully Adjustable", "Casual Styling"]
                }
            ]
        },
        "mild": {
            "tops": [
                {
                    "name": "Soft Cotton Knit Crewneck Sweater",
                    "brand": "Banana Republic",
                    "price": "$45.00",
                    "amazon_asin": "B01EXAMPLE2",
                    "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500",
                    "rating": 4.5,
                    "description": "A classic midweight cotton knit sweater that layers perfectly over a shirt.",
                    "features": ["100% Fine Knit Cotton", "Ribbed Collar & Hem", "Ultra-Soft Finish", "Resistant to Pilling"]
                }
            ],
            "bottoms": [
                {
                    "name": "Classic Straight-Fit Denim Jeans",
                    "brand": "Levi's",
                    "price": "$59.00",
                    "amazon_asin": "B08EXAMPLE2",
                    "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
                    "rating": 4.7,
                    "description": "The original straight-leg jeans. Rugged, durable, and universally stylish.",
                    "features": ["100% Rugged Cotton Denim", "Button Fly", "Classic 5-Pocket Styling", "Reinforced Copper Rivets"]
                }
            ],
            "footwear": [
                {
                    "name": "Retro Leather Lifestyle Sneakers",
                    "brand": "New Balance",
                    "price": "$75.00",
                    "amazon_asin": "B09EXAMPLE3",
                    "image": "https://images.unsplash.com/photo-1539185441755-769473a23570?w=500",
                    "rating": 4.6,
                    "description": "Premium leather and suede retro runners providing exceptional comfort.",
                    "features": ["Leather and Suede Upper", "Cushioned EVA Midsole", "Rubber Outsole", "Classic N Branding"]
                }
            ],
            "accessories": [
                {
                    "name": "Minimalist Leather Watch",
                    "brand": "MVMT",
                    "price": "$49.00",
                    "amazon_asin": "B01EXAMPLE3",
                    "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=500",
                    "rating": 4.3,
                    "description": "A clean, modern watch featuring a genuine leather strap and minimalist dial.",
                    "features": ["Quartz Movement", "Water Resistant (3ATM)", "Genuine Leather Strap", "Stainless Steel Case"]
                }
            ]
        },
        "cool": {
            "tops": [
                {
                    "name": "Sherpa-Lined Denim Trucker Jacket",
                    "brand": "Levi's",
                    "price": "$78.00",
                    "amazon_asin": "B07EXAMPLE3",
                    "image": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500",
                    "rating": 4.6,
                    "description": "The quintessential denim jacket lined with cozy warm sherpa fleece.",
                    "features": ["100% Cotton Denim", "Cozy Sherpa Fleece Lining", "Snap-Front Closure", "Dual Chest Pockets"]
                }
            ],
            "bottoms": [
                {
                    "name": "Comfort Stretch Corduroy Pants",
                    "brand": "Dockers",
                    "price": "$42.50",
                    "amazon_asin": "B08EXAMPLE3",
                    "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500",
                    "rating": 4.4,
                    "description": "Classic corduroy trousers designed with soft vertical wales and active stretch.",
                    "features": ["Fine Wale Corduroy", "Stretch Comfort Twill", "Classic Fit", "Machine Washable"]
                }
            ],
            "footwear": [
                {
                    "name": "Classic Suede Chelsea Boots",
                    "brand": "Clarks",
                    "price": "$89.99",
                    "amazon_asin": "B00EXAMPLE2",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.5,
                    "description": "Premium suede Chelsea boots featuring elastic side panels for easy wear.",
                    "features": ["Genuine Suede Leather", "Crepe Cushion Sole", "Elastic Gore Sides", "Pull Tab at Heel"]
                }
            ],
            "accessories": [
                {
                    "name": "Soft Knit Cashmere Scarf",
                    "brand": "Uniqlo",
                    "price": "$28.00",
                    "amazon_asin": "B07EXAMPLE4",
                    "image": "https://images.unsplash.com/photo-1520903074185-8eca362b3dce?w=500",
                    "rating": 4.4,
                    "description": "Ultra-soft cashmere feel scarf providing comforting neck warmth.",
                    "features": ["100% Cashmere-Feel Acrylic", "Fringe Detailing", "Generous Width", "Hand Wash Only"]
                }
            ]
        },
        "cold": {
            "tops": [
                {
                    "name": "Heavy Wool Blend Overcoat",
                    "brand": "Cole Haan",
                    "price": "$129.99",
                    "amazon_asin": "B00EXAMPLE3",
                    "image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=500",
                    "rating": 4.6,
                    "description": "Elegant wool-blend overcoat with quilted lining to block winter winds.",
                    "features": ["60% Wool, 40% Polyester", "Quilted Warm Lining", "Classic Button Closure", "Inner Security Pockets"]
                }
            ],
            "bottoms": [
                {
                    "name": "Fleece-Lined Relaxed Fit Jeans",
                    "brand": "Carhartt",
                    "price": "$65.00",
                    "amazon_asin": "B08EXAMPLE4",
                    "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
                    "rating": 4.7,
                    "description": "Heavyweight denim jeans lined with premium flannel-fleece for icy conditions.",
                    "features": ["12oz Ring-Spun Cotton Denim", "Polyester Fleece Lining", "Reinforced Back Pockets", "Triple-Stitched Seams"]
                }
            ],
            "footwear": [
                {
                    "name": "Waterproof Insulated Winter Boots",
                    "brand": "Sorel",
                    "price": "$110.00",
                    "amazon_asin": "B09EXAMPLE4",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.7,
                    "description": "Heavy-duty waterproof boots rated to keep feet dry in snow and slush.",
                    "features": ["Waterproof Leather Upper", "Seam-Sealed Construction", "100g Insulation", "Traction Rubber Lug Sole"]
                }
            ],
            "accessories": [
                {
                    "name": "Knit Wool Beanie & Touch Gloves",
                    "brand": "Carhartt",
                    "price": "$24.99",
                    "amazon_asin": "B07EXAMPLE5",
                    "image": "https://images.unsplash.com/photo-1576871337622-98d48d4aa53e?w=500",
                    "rating": 4.5,
                    "description": "Double-layer knit beanie bundled with touchscreen-compatible knit gloves.",
                    "features": ["Acrylic Rib-Knit", "Stretchable Comfort Fit", "Touchscreen-Friendly Finger Tips", "Wind-Resistant Knit"]
                }
            ]
        },
        "freezing": {
            "tops": [
                {
                    "name": "Sub-Zero Heavy Down Parka",
                    "brand": "The North Face",
                    "price": "$219.00",
                    "amazon_asin": "B08EXAMPLE5",
                    "image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=500",
                    "rating": 4.8,
                    "description": "Extreme cold down parka with waterproof DryVent shell and faux-fur hood.",
                    "features": ["550 Fill Goose Down", "Waterproof DryVent Shell", "Removable Faux-Fur Ruff", "Storm Flap Button Closure"]
                }
            ],
            "bottoms": [
                {
                    "name": "Insulated Thermal Utility Pants",
                    "brand": "Carhartt",
                    "price": "$69.50",
                    "amazon_asin": "B00EXAMPLE4",
                    "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500",
                    "rating": 4.6,
                    "description": "Heavy canvas cargo pants insulated with flannel to withstand freezing wind.",
                    "features": ["Ring-Spun Cotton Duck Canvas", "Soft Flannel Lining", "Multiple Tool & Utility Pockets", "Reinforced Knees"]
                }
            ],
            "footwear": [
                {
                    "name": "Sub-Zero Extreme Snow Boots",
                    "brand": "Kamik",
                    "price": "$125.00",
                    "amazon_asin": "B09EXAMPLE5",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.7,
                    "description": "Rubber bottom winter boots rated down to -40°F for extreme sub-zero protection.",
                    "features": ["Waterproof Nylon Upper", "Zylex Moisture-Wicking Liner", "Self-Cleaning Lug Outsole", "Adjustable Snow Collar"]
                }
            ],
            "accessories": [
                {
                    "name": "Thermal Balaclava & Ski Mittens",
                    "brand": "Tough Headwear",
                    "price": "$32.99",
                    "amazon_asin": "B01EXAMPLE4",
                    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500",
                    "rating": 4.5,
                    "description": "Full face balaclava paired with heavy duty thermal waterproof ski mittens.",
                    "features": ["Fleece Balaclava Mask", "Waterproof Shell Mittens", "Thinsulate Thermal Insulation", "Adjustable Wrist Straps"]
                }
            ]
        }
    },
    "formal": {
        "hot": {
            "tops": [
                {
                    "name": "Short Sleeve Linen Dress Shirt",
                    "brand": "Tommy Hilfiger",
                    "price": "$38.00",
                    "amazon_asin": "B07EXAMPLE6",
                    "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500",
                    "rating": 4.3,
                    "description": "A polished short sleeve shirt in breathable linen, perfect for summer weddings.",
                    "features": ["100% Linen", "Slim Fit", "Classic Collar", "Left Chest Pocket"]
                }
            ],
            "bottoms": [
                {
                    "name": "Lightweight Tailored Linen Pants",
                    "brand": "Perry Ellis",
                    "price": "$42.00",
                    "amazon_asin": "B08EXAMPLE6",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.2,
                    "description": "Linen dress trousers designed to keep you cool while maintaining formal lines.",
                    "features": ["Pure Linen Weave", "Flat Front Design", "Slanted Side Pockets", "Zip Fly Button Closure"]
                }
            ],
            "footwear": [
                {
                    "name": "Breathable Slip-On Loafers",
                    "brand": "Cole Haan",
                    "price": "$78.00",
                    "amazon_asin": "B09EXAMPLE6",
                    "image": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=500",
                    "rating": 4.4,
                    "description": "Perforated leather loafers that provide premium breathability and look highly polished.",
                    "features": ["Perforated Genuine Leather", "Grand.OS Comfort Tech", "Rubber Traction Pads", "Slip-On Design"]
                }
            ],
            "accessories": [
                {
                    "name": "Silk Pocket Square Set",
                    "brand": "Hextie",
                    "price": "$12.99",
                    "amazon_asin": "B01EXAMPLE5",
                    "image": "https://images.unsplash.com/photo-1520903074185-8eca362b3dce?w=500",
                    "rating": 4.5,
                    "description": "Pure silk colorful pocket squares to add a clean touch of class to summer suits.",
                    "features": ["100% Mulberry Silk", "Hand-Rolled Edges", "Standard Size", "Various Colors Included"]
                }
            ]
        },
        "warm": {
            "tops": [
                {
                    "name": "Premium Cotton Dress Shirt",
                    "brand": "Calvin Klein",
                    "price": "$45.00",
                    "amazon_asin": "B00EXAMPLE5",
                    "image": "https://images.unsplash.com/photo-1620012253295-c05518e993be?w=500",
                    "rating": 4.5,
                    "description": "Non-iron cotton dress shirt with a spread collar. Clean and professional.",
                    "features": ["100% Cotton", "Non-Iron Finish", "Spread Collar", "Slim Fit"]
                }
            ],
            "bottoms": [
                {
                    "name": "Tailored Flat-Front Dress Pants",
                    "brand": "Haggar",
                    "price": "$38.00",
                    "amazon_asin": "B08EXAMPLE7",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.4,
                    "description": "Wrinkle-free flat front trousers with an expandable waistband.",
                    "features": ["Premium Microfiber", "Expandable Waistband", "Wrinkle-Free", "Permanent Crease"]
                }
            ],
            "footwear": [
                {
                    "name": "Classic Oxford Dress Shoes",
                    "brand": "Bruno Marc",
                    "price": "$49.99",
                    "amazon_asin": "B00EXAMPLE6",
                    "image": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=500",
                    "rating": 4.5,
                    "description": "Elegant leather oxford lace-up dress shoes with a cushioned footbed.",
                    "features": ["Vegan/Genuine Leather options", "Wingtip Detailing", "Durable Outsole", "Breathable Lining"]
                }
            ],
            "accessories": [
                {
                    "name": "Genuine Leather Dress Belt",
                    "brand": "Timberland",
                    "price": "$18.50",
                    "amazon_asin": "B01EXAMPLE6",
                    "image": "https://images.unsplash.com/photo-1624222247344-550fb8ec5522?w=500",
                    "rating": 4.5,
                    "description": "Top-grain classic leather belt with a brushed silver buckle.",
                    "features": ["100% Genuine Leather", "Single-Prong Buckle", "Reinforced Stitching", "Width: 1.25 inches"]
                }
            ]
        },
        "mild": {
            "tops": [
                {
                    "name": "Modern Cut Herringbone Blazer",
                    "brand": "Tommy Hilfiger",
                    "price": "$95.00",
                    "amazon_asin": "B09EXAMPLE7",
                    "image": "https://images.unsplash.com/photo-1598808503742-dd34bd0444d0?w=500",
                    "rating": 4.6,
                    "description": "A structured herringbone blazer that dresses up any formal shirt-and-tie combo.",
                    "features": ["Polyester-Rayon Blend", "Two-Button Closure", "Notched Lapels", "Dual Vented Back"]
                }
            ],
            "bottoms": [
                {
                    "name": "Premium Stretch Suit Trousers",
                    "brand": "Calvin Klein",
                    "price": "$55.00",
                    "amazon_asin": "B08EXAMPLE8",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.4,
                    "description": "Slim suit pants with 4-way stretch fabric for comfortable elegance.",
                    "features": ["Polyester-Spandex Blend", "Slim Fit", "Flat Front", "Hidden Closure"]
                }
            ],
            "footwear": [
                {
                    "name": "Leather Monk Strap Dress Shoes",
                    "brand": "Bruno Marc",
                    "price": "$52.99",
                    "amazon_asin": "B00EXAMPLE7",
                    "image": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=500",
                    "rating": 4.5,
                    "description": "Stylish double monk strap dress shoes in premium burnished leather.",
                    "features": ["Genuine Leather Upper", "Double Buckle Straps", "Cushioned Footbed", "Flexible Rubber Sole"]
                }
            ],
            "accessories": [
                {
                    "name": "Premium Silk Necktie",
                    "brand": "Tommy Hilfiger",
                    "price": "$25.00",
                    "amazon_asin": "B07EXAMPLE7",
                    "image": "https://images.unsplash.com/photo-1520903074185-8eca362b3dce?w=500",
                    "rating": 4.6,
                    "description": "Pure jacquard silk tie featuring classic striped patterns.",
                    "features": ["100% Pure Silk", "Jacquard Weave", "Handmade Construction", "Standard Width: 3.25 inches"]
                }
            ]
        },
        "cool": {
            "tops": [
                {
                    "name": "Classic Double-Breasted Trench Coat",
                    "brand": "London Fog",
                    "price": "$115.00",
                    "amazon_asin": "B07EXAMPLE8",
                    "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500",
                    "rating": 4.6,
                    "description": "Water-repellent formal trench coat with zip-out insulated lining.",
                    "features": ["Water-Repellent Fabric", "Double-Breasted Design", "Adjustable Belt", "Zip-Out Warmer Liner"]
                }
            ],
            "bottoms": [
                {
                    "name": "Heavyweight Wool Suit Pants",
                    "brand": "Hart Schaffner Marx",
                    "price": "$68.00",
                    "amazon_asin": "B08EXAMPLE9",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.5,
                    "description": "Premium worsted wool dress trousers that provide heavy warmth.",
                    "features": ["100% Worsted Wool", "Fully Lined to Knee", "Classic Fit", "Slash Side Pockets"]
                }
            ],
            "footwear": [
                {
                    "name": "Smart Leather Dress Boots",
                    "brand": "Bruno Marc",
                    "price": "$65.00",
                    "amazon_asin": "B00EXAMPLE8",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.5,
                    "description": "Leather dress ankle boots with lace-up styling and zip side opening.",
                    "features": ["Genuine Leather Upper", "Side Zipper Access", "Chukka/Dress hybrid styling", "Treaded Sole"]
                }
            ],
            "accessories": [
                {
                    "name": "Fine Cashmere Scarf",
                    "brand": "State Cashmere",
                    "price": "$39.00",
                    "amazon_asin": "B01EXAMPLE7",
                    "image": "https://images.unsplash.com/photo-1520903074185-8eca362b3dce?w=500",
                    "rating": 4.7,
                    "description": "100% pure Inner Mongolian cashmere scarf, lightweight but incredibly warm.",
                    "features": ["100% Pure Cashmere", "Superb Insulation", "Unisex Style", "Dry Clean Recommended"]
                }
            ]
        },
        "cold": {
            "tops": [
                {
                    "name": "Double-Breasted Wool Overcoat",
                    "brand": "Cole Haan",
                    "price": "$149.00",
                    "amazon_asin": "B09EXAMPLE8",
                    "image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=500",
                    "rating": 4.6,
                    "description": "Warm, formal wool overcoat extending to the knee for full defense against cold winds.",
                    "features": ["Heavy Wool Blend", "Satin Lining", "Double-Breasted Lapels", "Slash Warmer Pockets"]
                }
            ],
            "bottoms": [
                {
                    "name": "Flannel-Lined Dress Trousers",
                    "brand": "Land's End",
                    "price": "$59.99",
                    "amazon_asin": "B08EXAMP10",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.5,
                    "description": "Elegant formal dress pants lined internally with premium lightweight flannel.",
                    "features": ["Worsted Wool Blend", "Premium Flannel Lining", "Flat Front", "Belt Loops"]
                }
            ],
            "footwear": [
                {
                    "name": "Shearling-Lined Leather Dress Boots",
                    "brand": "Allen Edmonds",
                    "price": "$135.00",
                    "amazon_asin": "B00EXAMPLE9",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.7,
                    "description": "High-end dress boots lined with genuine shearling fleece for cold business days.",
                    "features": ["Handcrafted Leather", "Shearling Fleece Lining", "Storm Welt Construction", "Rubber Grip Inlay"]
                }
            ],
            "accessories": [
                {
                    "name": "Genuine Leather Dress Gloves",
                    "brand": "Warmen",
                    "price": "$29.99",
                    "amazon_asin": "B01EXAMPLE8",
                    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500",
                    "rating": 4.4,
                    "description": "Sheepskin leather gloves with soft thermal cashmere lining.",
                    "features": ["Sheepskin Nappa Leather", "100% Cashmere Lining", "Touchscreen Capability", "Stitched Wrist Vent"]
                }
            ]
        },
        "freezing": {
            "tops": [
                {
                    "name": "Premium Cashmere Insulated Coat",
                    "brand": "Cole Haan",
                    "price": "$249.00",
                    "amazon_asin": "B07EXAMP10",
                    "image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=500",
                    "rating": 4.8,
                    "description": "Top-tier heavy coat made with rich cashmere wool fibers and a windproof inner bib.",
                    "features": ["Cashmere-Wool blend", "Windproof Zip-In Inner Bib", "Thinsulate Insulated Core", "Heavy Satin Lining"]
                }
            ],
            "bottoms": [
                {
                    "name": "Windproof Insulated Dress Trousers",
                    "brand": "Hart Schaffner Marx",
                    "price": "$89.99",
                    "amazon_asin": "B08EXAMP11",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.6,
                    "description": "Trousers lined with thermal micro-fleece to withstand freezing temperatures.",
                    "features": ["Worsted Wool Outer Shell", "Micro-Fleece Warm Inner Layer", "Tailored Fit", "Hook-and-Bar Closure"]
                }
            ],
            "footwear": [
                {
                    "name": "Waterproof Insulated Dress Chelsea Boots",
                    "brand": "Timberland",
                    "price": "$129.99",
                    "amazon_asin": "B00EXAMP10",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.6,
                    "description": "Seam-sealed Chelsea dress boots with 200g PrimaLoft insulation.",
                    "features": ["Waterproof Seam-Sealed Leather", "200g PrimaLoft Insulation", "Anti-Fatigue Footbed", "Recycled Rubber Outsole"]
                }
            ],
            "accessories": [
                {
                    "name": "Cashmere Knit Beanie & Wool Scarf",
                    "brand": "State Cashmere",
                    "price": "$48.00",
                    "amazon_asin": "B01EXAMP10",
                    "image": "https://images.unsplash.com/photo-1576871337622-98d48d4aa53e?w=500",
                    "rating": 4.7,
                    "description": "Cashmere knit beanie paired with a heavy formal knit wool scarf.",
                    "features": ["100% Cashmere Beanie", "Pure Merino Wool Scarf", "Ribbed Cozy Knit", "Elegant Gift Packaging"]
                }
            ]
        }
    },
    "sporty": {
        "hot": {
            "tops": [
                {
                    "name": "Dry-Fit Moisture-Wicking Singlet",
                    "brand": "Nike",
                    "price": "$22.00",
                    "amazon_asin": "B07EXAMPLE9",
                    "image": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500",
                    "rating": 4.5,
                    "description": "Ultra-light active tank top that wicks sweat and dries instantly.",
                    "features": ["100% Polyester Dry-Fit", "Mesh Back Ventilation", "Flatlock Seams", "Reflective Swoosh"]
                }
            ],
            "bottoms": [
                {
                    "name": "Performance Active Running Shorts",
                    "brand": "Under Armour",
                    "price": "$24.99",
                    "amazon_asin": "B08EXAMP12",
                    "image": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500",
                    "rating": 4.4,
                    "description": "Ultra-light athletic shorts with built-in compression lining.",
                    "features": ["Moisture Wicking Fabric", "Internal Mesh Brief Liner", "4-Way Stretch Construction", "Elastic Waistband"]
                }
            ],
            "footwear": [
                {
                    "name": "Lightweight Cushioned Trainer Shoes",
                    "brand": "Adidas",
                    "price": "$65.00",
                    "amazon_asin": "B09EXAMPLE9",
                    "image": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=500",
                    "rating": 4.6,
                    "description": "Ultra-cushioned running trainers with mesh uppers for hot weather ventilation.",
                    "features": ["Breathable Knit Mesh Upper", "Cloudfoam Cushioned Sole", "Ortholite Sockliner", "Durable Traction Outsole"]
                }
            ],
            "accessories": [
                {
                    "name": "Aerobill Featherlight Running Cap",
                    "brand": "Nike",
                    "price": "$19.99",
                    "amazon_asin": "B01EXAMPLE9",
                    "image": "https://images.unsplash.com/photo-1534215754734-18e55d13e346?w=500",
                    "rating": 4.4,
                    "description": "Perforated lightweight cap with moisture sweatband.",
                    "features": ["Featherlight construction", "Dri-FIT sweatband", "Perforated side panels", "Adjustable hook loop strap"]
                }
            ]
        },
        "warm": {
            "tops": [
                {
                    "name": "Performance Tech T-Shirt",
                    "brand": "Under Armour",
                    "price": "$25.00",
                    "amazon_asin": "B00EXAMPLE7",
                    "image": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500",
                    "rating": 4.5,
                    "description": "UA Tech fabric tee that feels ultra-soft and has a natural feel.",
                    "features": ["UA Tech Quick-Dry Fabric", "Anti-Odor Technology", "Ergonomic Flat Seams", "Relaxed Athletic Fit"]
                }
            ],
            "bottoms": [
                {
                    "name": "Athletic Flex Gym Shorts",
                    "brand": "Nike",
                    "price": "$28.00",
                    "amazon_asin": "B08EXAMP13",
                    "image": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500",
                    "rating": 4.5,
                    "description": "Flexible woven athletic shorts designed for gym training or running.",
                    "features": ["Dri-FIT Technology", "Side Hem Vents for movement", "Zippered Side Pockets", "Elastic Drawcord Waist"]
                }
            ],
            "footwear": [
                {
                    "name": "Running Support Cushion Sneakers",
                    "brand": "Asics",
                    "price": "$79.99",
                    "amazon_asin": "B00EXAMPLE8",
                    "image": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=500",
                    "rating": 4.7,
                    "description": "Highly comfortable road running shoes featuring supportive GEL cushioning.",
                    "features": ["Rearfoot GEL Cushioning System", "Engineered Mesh Upper", "Amplifoam Midsole", "Guidance Line Midsole Tech"]
                }
            ],
            "accessories": [
                {
                    "name": "Fitness & Activity Smartwatch",
                    "brand": "Fitbit",
                    "price": "$89.00",
                    "amazon_asin": "B01EXAMP11",
                    "image": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500",
                    "rating": 4.5,
                    "description": "Waterproof fitness tracker with heart rate and sleep monitoring.",
                    "features": ["Built-in GPS", "24/7 Heart Rate Monitor", "Active Zone Minutes Tracker", "7-Day Battery Life"]
                }
            ]
        },
        "mild": {
            "tops": [
                {
                    "name": "Tech Fleece Hooded Jacket",
                    "brand": "Nike",
                    "price": "$65.00",
                    "amazon_asin": "B09EXAMP10",
                    "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500",
                    "rating": 4.6,
                    "description": "Premium lightweight warmth zip hoodie. Modern double-sided spacer fabric.",
                    "features": ["Double-sided spacer fleece", "Full zip hood", "Zippered sleeve pocket", "Athletic styling"]
                }
            ],
            "bottoms": [
                {
                    "name": "Tapered Performance Joggers",
                    "brand": "Adidas",
                    "price": "$45.00",
                    "amazon_asin": "B08EXAMP14",
                    "image": "https://images.unsplash.com/photo-1515434126000-961d90ff09db?w=500",
                    "rating": 4.5,
                    "description": "Tapered leg joggers with zip ankles for athletic mobility.",
                    "features": ["AeroReady Moisture Wicking", "Zip ankle hems", "Side zipper pockets", "Drawstring closure"]
                }
            ],
            "footwear": [
                {
                    "name": "Comfort Foam Training Sneakers",
                    "brand": "Under Armour",
                    "price": "$68.00",
                    "amazon_asin": "B00EXAMP11",
                    "image": "https://images.unsplash.com/photo-1539185441755-769473a23570?w=500",
                    "rating": 4.5,
                    "description": "Comfortable cross-training shoes with a responsive Charged Cushioning midsole.",
                    "features": ["Charged Cushioning Midsole", "Durable Rubber Grip Outsole", "Breathable Mesh Inlay", "Heel Pull Tab"]
                }
            ],
            "accessories": [
                {
                    "name": "Sweat-Wicking Athletic Headband",
                    "brand": "Under Armour",
                    "price": "$12.99",
                    "amazon_asin": "B07EXAMPLE9",
                    "image": "https://images.unsplash.com/photo-1520903074185-8eca362b3dce?w=500",
                    "rating": 4.3,
                    "description": "Comfortable non-slip athletic headband to keep sweat away.",
                    "features": ["Silicone Grip Strip", "Quick-Dry Elastic fabric", "Unisex styling", "Pack of 2"]
                }
            ]
        },
        "cool": {
            "tops": [
                {
                    "name": "Water-Resistant Athletic Windbreaker",
                    "brand": "Columbia",
                    "price": "$55.00",
                    "amazon_asin": "B07EXAMP11",
                    "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500",
                    "rating": 4.5,
                    "description": "Lightweight windproof jacket featuring water-resistant material and an adjustable hood.",
                    "features": ["Omni-Shield Water Repellent", "Drawcord Adjustable Hood", "Zippered Hand Pockets", "Elastic Cuffs"]
                }
            ],
            "bottoms": [
                {
                    "name": "Fleece Workout Jogger Pants",
                    "brand": "Under Armour",
                    "price": "$39.99",
                    "amazon_asin": "B08EXAMP15",
                    "image": "https://images.unsplash.com/photo-1515434126000-961d90ff09db?w=500",
                    "rating": 4.5,
                    "description": "Soft fleece pants with high heat retention for cool weather jogging.",
                    "features": ["Armour Fleece construction", "Soft inner layer traps heat", "Elastic waistband", "Open hand pockets"]
                }
            ],
            "footwear": [
                {
                    "name": "All-Terrain Trail Running Shoes",
                    "brand": "Salomon",
                    "price": "$95.00",
                    "amazon_asin": "B00EXAMP12",
                    "image": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=500",
                    "rating": 4.6,
                    "description": "Grip-focused trail shoes built for off-road training in cool conditions.",
                    "features": ["Contagrip Mud & Wet Traction", "Quicklace System", "SensiFit support wings", "Protective Toe Cap"]
                }
            ],
            "accessories": [
                {
                    "name": "Thermal Running Glove Liners",
                    "brand": "Under Armour",
                    "price": "$19.99",
                    "amazon_asin": "B01EXAMP12",
                    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500",
                    "rating": 4.4,
                    "description": "Slim, touch-screen compatible thermal gloves perfect for outdoor training.",
                    "features": ["ColdGear Fleece Lining", "Touchscreen Index & Thumb", "Reflective Details", "Silicone Palm Print"]
                }
            ]
        },
        "cold": {
            "tops": [
                {
                    "name": "Insulated Active Puffer Jacket",
                    "brand": "Columbia",
                    "price": "$119.00",
                    "amazon_asin": "B09EXAMP11",
                    "image": "https://images.unsplash.com/photo-1611312449412-6cefac5dc3e4?w=500",
                    "rating": 4.6,
                    "description": "Puffer jacket with Omni-Heat reflective lining to maximize active heat retention.",
                    "features": ["Omni-Heat Reflective Tech", "Water-Resistant fabric", "Synthetic Down insulation", "Zippered pockets"]
                }
            ],
            "bottoms": [
                {
                    "name": "Thermal Fleece-Lined Compression Pants",
                    "brand": "Under Armour",
                    "price": "$49.50",
                    "amazon_asin": "B08EXAMP16",
                    "image": "https://images.unsplash.com/photo-1515434126000-961d90ff09db?w=500",
                    "rating": 4.6,
                    "description": "ColdGear compression leggings lined with brushed micro-fleece to wear under gym shorts.",
                    "features": ["Dual-Layer ColdGear Fabric", "Brushed Fleece Interior", "4-Way Stretch fabric", "Mock fly seams"]
                }
            ],
            "footwear": [
                {
                    "name": "Winterized Gore-Tex Trail Runners",
                    "brand": "Salomon",
                    "price": "$120.00",
                    "amazon_asin": "B00EXAMP13",
                    "image": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=500",
                    "rating": 4.7,
                    "description": "Waterproof Gore-Tex trail runner shoes designed to keep feet warm and dry in wet snow.",
                    "features": ["Gore-Tex Waterproofing", "Contagrip Traction Outsole", "ClimaSalomon insulation", "OrthoLite Sockliner"]
                }
            ],
            "accessories": [
                {
                    "name": "Fleece Knit Beanie Hat",
                    "brand": "The North Face",
                    "price": "$22.00",
                    "amazon_asin": "B01EXAMP13",
                    "image": "https://images.unsplash.com/photo-1576871337622-98d48d4aa53e?w=500",
                    "rating": 4.6,
                    "description": "A high-insulating fleece beanie designed to retain body heat during cold weather jogs.",
                    "features": ["100% Recycled Polyester Fleece", "Snug athletic fit", "Embroidered Logo", "Flatlock Seams"]
                }
            ]
        },
        "freezing": {
            "tops": [
                {
                    "name": "Extreme Cold Weather Insulated Ski Jacket",
                    "brand": "Columbia",
                    "price": "$189.00",
                    "amazon_asin": "B07EXAMP12",
                    "image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=500",
                    "rating": 4.7,
                    "description": "Advanced thermal insulated jacket with fully sealed seams and powder skirt.",
                    "features": ["Omni-Tech Waterproof Shell", "80g Microtemp insulation", "Removable Adjustable Hood", "Underarm Venting"]
                }
            ],
            "bottoms": [
                {
                    "name": "Waterproof Insulated Snow Pants",
                    "brand": "Arctix",
                    "price": "$45.00",
                    "amazon_asin": "B08EXAMP17",
                    "image": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500",
                    "rating": 4.5,
                    "description": "Highly durable windproof and waterproof ski/snowboard trousers.",
                    "features": ["ThermaLock Waterproof Shell", "85g ThermaTech Insulation", "Boot Gaiters with Grippers", "Reinforced Scuff Guards"]
                }
            ],
            "footwear": [
                {
                    "name": "Waterproof Snow Hiking Boots",
                    "brand": "Sorel",
                    "price": "$125.00",
                    "amazon_asin": "B00EXAMP14",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.7,
                    "description": "Heavy-duty waterproof hiking boots featuring deep winter rubber treads and thick fleece liners.",
                    "features": ["Waterproof Nylon & Leather", "Thick Removable Felt Liner", "Handcrafted Rubber Shell", "D-Ring Lace System"]
                }
            ],
            "accessories": [
                {
                    "name": "Anti-Fog Snow Goggles & Balaclava",
                    "brand": "Zionor",
                    "price": "$38.50",
                    "amazon_asin": "B01EXAMP14",
                    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500",
                    "rating": 4.5,
                    "description": "Double lens anti-fog winter goggles bundled with a protective micro-fleece thermal face mask.",
                    "features": ["UV400 Protection Goggles", "Spherical Wide View Lens", "Brushed Fleece Balaclava", "Adjustable Elastic Strap"]
                }
            ]
        }
    },
    "trendy": {
        "hot": {
            "tops": [
                {
                    "name": "Oversized Knit Boxy Tee",
                    "brand": "Urban Outfitters",
                    "price": "$28.00",
                    "amazon_asin": "B07EXAMP13",
                    "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
                    "rating": 4.4,
                    "description": "A stylish oversized crop graphic/boxy tee made with soft heavy-gauge cotton.",
                    "features": ["Heavyweight Cotton", "Drop-Shoulder Cut", "Distressed detailing", "Retro Graphic Front"]
                }
            ],
            "bottoms": [
                {
                    "name": "Distressed Raw-Hem Denim Shorts",
                    "brand": "Levi's",
                    "price": "$45.00",
                    "amazon_asin": "B08EXAMP18",
                    "image": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500",
                    "rating": 4.5,
                    "description": "High-rise denim shorts with custom shredded detailing and raw hem edge.",
                    "features": ["100% Rigid Denim", "High-Rise Cut", "Frayed Raw Hem", "Button Fly"]
                }
            ],
            "footwear": [
                {
                    "name": "Chunky Platform EVA Sandals",
                    "brand": "Doc Martens",
                    "price": "$65.00",
                    "amazon_asin": "B09EXAMP12",
                    "image": "https://images.unsplash.com/photo-1603487226258-414a77935767?w=500",
                    "rating": 4.3,
                    "description": "Chunky lightweight platform sandals with adjustable buckle strap closures.",
                    "features": ["EVA Platform Midsole", "Synthetic Strap Upper", "Triple-strap design", "Cushioned Footbed"]
                }
            ],
            "accessories": [
                {
                    "name": "Reversible Cotton Bucket Hat",
                    "brand": "Champion",
                    "price": "$18.00",
                    "amazon_asin": "B01EXAMP15",
                    "image": "https://images.unsplash.com/photo-1534215754734-18e55d13e346?w=500",
                    "rating": 4.4,
                    "description": "Classic nineties-style reversible cotton twill bucket hat.",
                    "features": ["100% Cotton Twill", "Embroidered eyelets", "Unisex styling", "Packable construction"]
                }
            ]
        },
        "warm": {
            "tops": [
                {
                    "name": "Oversized Lightweight Linen Shacket",
                    "brand": "Zara",
                    "price": "$42.00",
                    "amazon_asin": "B00EXAMP15",
                    "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500",
                    "rating": 4.3,
                    "description": "A lightweight oversized button-down shirt that functions as a light summer jacket.",
                    "features": ["Linen blend fabric", "Oversized utility cut", "Front flap pockets", "Drop shoulder"]
                }
            ],
            "bottoms": [
                {
                    "name": "Wide-Leg Skate Utility Cargo Pants",
                    "brand": "Dickies",
                    "price": "$49.99",
                    "amazon_asin": "B08EXAMP19",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.4,
                    "description": "Retro skater wide-leg cargo trousers in heavyweight cotton canvas.",
                    "features": ["Heavy Cotton Canvas", "Dual Utility Cargo pockets", "Hammer Loop detail", "Relaxed Wide Leg"]
                }
            ],
            "footwear": [
                {
                    "name": "Chunky Retro Dad Sneakers",
                    "brand": "Fila",
                    "price": "$68.00",
                    "amazon_asin": "B00EXAMP16",
                    "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500",
                    "rating": 4.5,
                    "description": "Thick platform runner shoes featuring chunky rubber sole outlines.",
                    "features": ["Synthetic leather upper", "Lightweight EVA midsole", "Chunky rubber tread", "Embossed branding"]
                }
            ],
            "accessories": [
                {
                    "name": "Retro Rectangular Sunglasses",
                    "brand": "Ray-Ban",
                    "price": "$24.99",
                    "amazon_asin": "B01EXAMP16",
                    "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500",
                    "rating": 4.5,
                    "description": "Retro nineties rectangular sunglasses with colored lenses and thick frames.",
                    "features": ["Thick Acetate frame", "Non-polarized UV Protection", "Retro rectangular profile", "Unisex design"]
                }
            ]
        },
        "mild": {
            "tops": [
                {
                    "name": "Distressed Faux-Leather Moto Jacket",
                    "brand": "Zara",
                    "price": "$95.00",
                    "amazon_asin": "B09EXAMP12",
                    "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500",
                    "rating": 4.5,
                    "description": "Edgy faux-leather motorcycle jacket with metallic zipper hardware.",
                    "features": ["Vegan polyurethane leather", "Asymmetrical front zipper", "Zipper pockets", "Quilted shoulder panels"]
                }
            ],
            "bottoms": [
                {
                    "name": "Straight-Leg Vintage Wash Jeans",
                    "brand": "Levi's",
                    "price": "$68.00",
                    "amazon_asin": "B08EXAMP20",
                    "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
                    "rating": 4.6,
                    "description": "Light wash straight leg denim jeans with subtle vintage distressing.",
                    "features": ["100% Cotton Denim", "Classic straight-leg cut", "Vintage wash effect", "Reinforced stitching"]
                }
            ],
            "footwear": [
                {
                    "name": "High-Top Vintage Canvas Sneakers",
                    "brand": "Converse",
                    "price": "$55.00",
                    "amazon_asin": "B00EXAMP17",
                    "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500",
                    "rating": 4.6,
                    "description": "Classic Chuck Taylor high-top sneakers with retro canvas styling.",
                    "features": ["High-top ankle collar", "Durable Canvas Upper", "Classic Star Ankle patch", "Rubber toe cap"]
                }
            ],
            "accessories": [
                {
                    "name": "Canvas Sling Crossbody Bag",
                    "brand": "Carhartt",
                    "price": "$29.00",
                    "amazon_asin": "B01EXAMP17",
                    "image": "https://images.unsplash.com/photo-1624222247344-550fb8ec5522?w=500",
                    "rating": 4.4,
                    "description": "Minimalist canvas utility sling bag with robust metal zip compartments.",
                    "features": ["Heavy Duty Canvas", "Adjustable Webbing strap", "Main zippered compartment", "Embroidered patch"]
                }
            ]
        },
        "cool": {
            "tops": [
                {
                    "name": "Oversized Corduroy Utility Shacket",
                    "brand": "Urban Outfitters",
                    "price": "$58.00",
                    "amazon_asin": "B07EXAMP14",
                    "image": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500",
                    "rating": 4.4,
                    "description": "A heavy wale corduroy oversized shirt-jacket. Cozy and highly stylish.",
                    "features": ["Thick Wale Corduroy", "Snap front closure", "Dual oversized pockets", "Frayed bottom hem"]
                }
            ],
            "bottoms": [
                {
                    "name": "Tapered Cotton Utility Cargo Pants",
                    "brand": "Dickies",
                    "price": "$45.00",
                    "amazon_asin": "B08EXAMP21",
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",
                    "rating": 4.4,
                    "description": "Tapered leg cargo utility pants with reinforced pocket lining.",
                    "features": ["100% Cotton Ripstop twill", "Adjustable waist tabs", "Drawstring ankle cuffs", "Reinforced seat"]
                }
            ],
            "footwear": [
                {
                    "name": "Chunky Platform Leather Combat Boots",
                    "brand": "Doc Martens",
                    "price": "$129.99",
                    "amazon_asin": "B00EXAMP18",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.7,
                    "description": "Iconic high platform leather combat boots with yellow stitching.",
                    "features": ["Genuine Patent Leather", "Bouncing Lug Sole", "Yellow Welt Stitching", "High Platform: 1.5 inches"]
                }
            ],
            "accessories": [
                {
                    "name": "Rib-Knit Fisherman Beanie",
                    "brand": "Carhartt",
                    "price": "$19.00",
                    "amazon_asin": "B01EXAMP18",
                    "image": "https://images.unsplash.com/photo-1576871337622-98d48d4aa53e?w=500",
                    "rating": 4.5,
                    "description": "A shallow-fit short fisherman beanie in tight rib-knit weave.",
                    "features": ["Acrylic Rib-Knit", "Shallow Fisherman crown", "Foldable thick brim", "Snug comfortable fit"]
                }
            ]
        },
        "cold": {
            "tops": [
                {
                    "name": "Faux-Shearling Aviator Jacket",
                    "brand": "Alpha Industries",
                    "price": "$179.00",
                    "amazon_asin": "B09EXAMP13",
                    "image": "https://images.unsplash.com/photo-1608063615781-e2ef8c73d114?w=500",
                    "rating": 4.6,
                    "description": "Stunning retro B-3 style faux-leather bomber jacket with plush fleece shearling collar.",
                    "features": ["Thick faux-leather shell", "Warm faux-shearling lining", "Buckled collar straps", "Adjustable side belts"]
                }
            ],
            "bottoms": [
                {
                    "name": "Heavy Denim Cargo Jeans",
                    "brand": "Levis",
                    "price": "$75.00",
                    "amazon_asin": "B08EXAMP22",
                    "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
                    "rating": 4.5,
                    "description": "Robust heavy cotton denim pants with button-flap side cargo compartments.",
                    "features": ["100% Cotton Heavy Denim", "Dual cargo utility pockets", "Relaxed fit", "Contrast stitch lines"]
                }
            ],
            "footwear": [
                {
                    "name": "Chunky platform lug sole boots",
                    "brand": "Steve Madden",
                    "price": "$95.00",
                    "amazon_asin": "B00EXAMP19",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.5,
                    "description": "High platform leather ankle boots with thick chunky serrated tread soles.",
                    "features": ["Waterproof Leather Upper", "Side elastic stretch panels", "Serrated thick lug tread", "Fleece insoles"]
                }
            ],
            "accessories": [
                {
                    "name": "Patterned Knit Winter Scarf",
                    "brand": "Pendleton",
                    "price": "$38.00",
                    "amazon_asin": "B01EXAMP19",
                    "image": "https://images.unsplash.com/photo-1520903074185-8eca362b3dce?w=500",
                    "rating": 4.6,
                    "description": "Heavy knit jacquard wool scarf featuring colorful geo-tribal patterns.",
                    "features": ["Worsted wool blend", "Jacquard patterned weave", "Generous length: 70 inches", "Hand wash only"]
                }
            ]
        },
        "freezing": {
            "tops": [
                {
                    "name": "Metallic Oversized Puffer Coat",
                    "brand": "The North Face",
                    "price": "$249.00",
                    "amazon_asin": "B07EXAMP15",
                    "image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=500",
                    "rating": 4.8,
                    "description": "High-shine metallic puffer coat packed with goose down to withstand freezing temps.",
                    "features": ["Shiny metallic water-repellent shell", "700 Fill Down insulation", "Stowable hood", "Adjustable waist drawcord"]
                }
            ],
            "bottoms": [
                {
                    "name": "Quilted Insulated Sweatpants",
                    "brand": "Nike",
                    "price": "$85.00",
                    "amazon_asin": "B08EXAMP23",
                    "image": "https://images.unsplash.com/photo-1515434126000-961d90ff09db?w=500",
                    "rating": 4.5,
                    "description": "Quilted trousers lined with light synthetic fill for cozy freezing-weather walks.",
                    "features": ["Therma-FIT Heat Retention", "Synthetic fill padding", "Ribbed knit cuffs", "Side zipper pockets"]
                }
            ],
            "footwear": [
                {
                    "name": "Insulated Platform Designer Snow Boots",
                    "brand": "Moon Boot",
                    "price": "$159.00",
                    "amazon_asin": "B00EXAMP20",
                    "image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500",
                    "rating": 4.7,
                    "description": "Iconic high-top padded snow boots with heavy criss-cross lacing.",
                    "features": ["Waterproof nylon fabric", "Padded foam thermal lining", "Platform rubber grip outsole", "Unisex chunky profile"]
                }
            ],
            "accessories": [
                {
                    "name": "Statement Faux Fur Trapper Hat",
                    "brand": "Mad Bomber",
                    "price": "$39.00",
                    "amazon_asin": "B01EXAMP20",
                    "image": "https://images.unsplash.com/photo-1576871337622-98d48d4aa53e?w=500",
                    "rating": 4.6,
                    "description": "Luxury statement trapper hat lined with soft windproof faux-fur.",
                    "features": ["Waterproof Nylon crown", "Premium Faux-Fur trim", "Ear flaps with chin buckle", "Thermal fleece lining"]
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
        # Fallback values if style or temp not found
        s = style.lower() if style else "casual"
        if s not in AFFILIATE_PRODUCTS:
            s = "casual"
            
        t = temperature_category.lower() if temperature_category else "warm"
        if t not in AFFILIATE_PRODUCTS[s]:
            # Fallbacks for temperature mismatch
            if t in ["cold", "freezing"] and "cool" in AFFILIATE_PRODUCTS[s]:
                t = "cool"
            elif t in ["hot", "warm"] and "warm" in AFFILIATE_PRODUCTS[s]:
                t = "warm"
            else:
                t = list(AFFILIATE_PRODUCTS[s].keys())[0]
                
        products = AFFILIATE_PRODUCTS[s][t]
        
        # Format structures and add affiliate URLs
        formatted_products = {}
        for cat in ["tops", "bottoms", "footwear", "accessories"]:
            formatted_products[cat] = []
            if cat in products:
                for product in products[cat]:
                    # Create a copy to prevent in-place mutation of db
                    p = dict(product)
                    if 'amazon_asin' in p:
                        p['affiliateUrl'] = generate_affiliate_url(p['amazon_asin'])
                    else:
                        p['affiliateUrl'] = '#'
                    formatted_products[cat].append(p)
                    
        return formatted_products
    except Exception as e:
        print(f"Error getting products: {e}")
        return {'tops': [], 'bottoms': [], 'footwear': [], 'accessories': []}