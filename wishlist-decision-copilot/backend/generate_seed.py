import json
import random

categories = [
    {"category": "Dresses", "gender": "Women", "brands": ["Mode Studio", "DressBerry", "Willow & Co.", "Urban Thread"], "images": ["https://images.unsplash.com/photo-1595777457583-95e059d581b8", "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1", "https://images.unsplash.com/photo-1539008835657-9e8e9680c956"]},
    {"category": "Trousers", "gender": "Men", "brands": ["Northline", "Roadster", "StreetForm", "Vela"], "images": ["https://images.unsplash.com/photo-1624378439575-d8705ad7ae80", "https://images.unsplash.com/photo-1473966968600-fa801b869a1a", "https://images.unsplash.com/photo-1555689502-c4b22d76c56f"]},
    {"category": "Sneakers", "gender": "Unisex", "brands": ["Puma", "Nike", "Vela", "StreetForm"], "images": ["https://images.unsplash.com/photo-1542291026-7eec264c27ff", "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2", "https://images.unsplash.com/photo-1608231387042-66d1773070a5"]},
    {"category": "Tops", "gender": "Women", "brands": ["Mango", "ONLY", "Willow & Co.", "Mode Studio"], "images": ["https://images.unsplash.com/photo-1503342217505-b0a15ec3261c", "https://images.unsplash.com/photo-1434389670869-bac08581138c", "https://images.unsplash.com/photo-1485230895905-eb56ba859426"]},
    {"category": "Jackets", "gender": "Men", "brands": ["Levi's", "Northline", "WROGN", "Urban Thread"], "images": ["https://images.unsplash.com/photo-1551028719-01c86b24bb6a", "https://images.unsplash.com/photo-1591047139829-d91aecb6caea", "https://images.unsplash.com/photo-1520975954732-57dd22299614"]},
    {"category": "Bags", "gender": "Women", "brands": ["Coastline", "Caprese", "Vela", "Mode Studio"], "images": ["https://images.unsplash.com/photo-1584916201218-f4242ceb4809", "https://images.unsplash.com/photo-1591561954557-26941169b49e", "https://images.unsplash.com/photo-1548036328-c9fa89d128fa"]},
]

products = []
id_counter = 1

for cat in categories:
    for i in range(6):
        base_price = random.randint(1000, 5000)
        has_discount = random.choice([True, False])
        original_price = base_price + random.randint(500, 2000) if has_discount else None
        rating = round(random.uniform(3.5, 4.9), 1)
        reviews = random.randint(10, 2500)
        
        # 3 variations of the same Unsplash image based on URL query params for a realistic gallery feel without finding 100 images
        base_img = random.choice(cat["images"])
        images = [
            f"{base_img}?w=800&q=80",
            f"{base_img}?w=800&q=80&fit=crop&crop=focalpoint",
            f"{base_img}?w=800&q=80&fit=crop&crop=edges"
        ]
        
        brand = random.choice(cat["brands"])
        
        quality_score = "High" if rating > 4.2 else "Medium"
        value_score = "Excellent" if has_discount and rating > 4.0 else "Average"
        
        p = {
            "name": f"{brand} {cat['gender']} Premium {cat['category']} {i+1}",
            "brand": brand,
            "category": cat["category"],
            "gender": cat["gender"],
            "price": float(base_price),
            "original_price": float(original_price) if original_price else None,
            "rating": rating,
            "review_count": reviews,
            "fit": random.choice(["Regular", "Slim", "Oversized", "True to size"]),
            "material": random.choice(["100% Cotton", "Polyester Blend", "Premium Leather", "Denim", "Canvas"]),
            "color": random.choice(["Black", "Navy", "White", "Olive", "Maroon"]),
            "availability": "In Stock" if random.random() > 0.1 else "Few left",
            "description": f"Experience the perfect blend of comfort and style with this premium offering from {brand}. Designed for modern {cat['gender'].lower()} who appreciate quality.",
            "images": images,
            "sizes": ["S", "M", "L", "XL", "XXL"] if cat["category"] not in ["Bags", "Sneakers"] else ["7", "8", "9", "10", "11"] if cat["category"] == "Sneakers" else ["One Size"],
            "quality_signals": {"material_quality": quality_score, "durability": quality_score},
            "value_signals": {"price_competitiveness": value_score, "discount_active": has_discount},
            "review_signals": {"positive_sentiment": int(rating * 20), "common_praise": "Comfortable fit" if rating > 4.0 else "Decent for price"}
        }
        products.append(p)
        id_counter += 1

with open("demo_products.json", "w") as f:
    json.dump(products, f, indent=2)
print("Generated 36 products")
