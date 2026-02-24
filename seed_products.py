import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_app.settings')
django.setup()

from products.models import Category, Product
from django.utils.text import slugify
import urllib.request
from django.core.files.base import ContentFile

def seed_data():
    print("Generating 50 new products...")

    categories = [
        "Electronics", "Fashion", "Home & Living", "Beauty", "Sports"
    ]
    
    # Ensure categories exist
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name)

    adjectives = ["Premium", "Essential", "Minimalist", "Ergonomic", "Smart", "Ultra", "Classic", "Organic", "Hydrating", "Wireless"]
    nouns = ["Device", "Kit", "Set", "Pack", "System", "Gear", "Tool", "Accessory", "Item", "Bundle"]

    for i in range(50):
        cat_name = random.choice(categories)
        cat = Category.objects.get(name=cat_name)
        
        name = f"{random.choice(adjectives)} {cat_name[:-1]} {random.choice(nouns)} {random.randint(100, 999)}"
        price = round(random.uniform(15.0, 500.0), 2)
        
        # 30% chance to have a discount
        discount_price = None
        is_on_sale = False
        sale_badge_text = ""
        if random.random() < 0.3:
            discount_price = round(price * random.uniform(0.6, 0.9), 2)
            is_on_sale = True
            sale_badge_text = random.choice(["Sale!", "Limited Offer", "Clearance"])

        stock = random.randint(5, 150)

        product = Product.objects.create(
            category=cat,
            name=name,
            price=price,
            discount_price=discount_price,
            stock=stock,
            description=f"This is a newly added {name} from our {cat_name} collection.",
            is_available=True,
            is_on_sale=is_on_sale,
            sale_badge_text=sale_badge_text
        )
        
        # print(f"Fetching image for {name}...")
        image_url = f"https://picsum.photos/600/400?random={random.randint(1, 10000)}"
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            product.image.save(f"{slugify(name)}.jpg", ContentFile(response.read()), save=True)
            print(f"[{i+1}/50] Created Product: {name} with image")
        except Exception as e:
            print(f"[{i+1}/50] Created Product: {name} (Image failed: {e})")

    print("50 new products have been seeded!")

if __name__ == "__main__":
    seed_data()
