# --- Run this in 'python manage.py shell' ---
# First, import all the models
from api.models import Brand, Category, Pen, PenRefill
from api.constants import DEFAULT_CATEGORIES

# --- Step 1: Create Categories ---
# We use get_or_create so you can run this script
# multiple times without creating duplicates.

cat_pen, created = Category.objects.get_or_create(
  name=DEFAULT_CATEGORIES[0].name,
  description=DEFAULT_CATEGORIES[0].description
)

cat_refill, created = Category.objects.get_or_create(
  name=DEFAULT_CATEGORIES[1].name,
  description=DEFAULT_CATEGORIES[1].description
)

# --- Step 2: Create Brands ---
brand_pilot, created = Brand.objects.get_or_create(
  name="Pilot",
  description="Popular Japanese pen manufacturer, known for G2."
)

brand_uniball, created = Brand.objects.get_or_create(
  name="Uni-ball",
  description="Known for the Signo and Jetstream lines."
)

brand_zebra, created = Brand.objects.get_or_create(
  name="Zebra",
  description="Japanese manufacturer, known for Sarasa and Mildliner."
)

brand_lamy, created = Brand.objects.get_or_create(
  name="Lamy",
  description="German brand known for the Safari fountain pen."
)

print("--- Created Brands and Categories ---")

# --- Step 3: Create Pen Instances ---
Pen.objects.get_or_create(
  name="Pilot G2 07",
  defaults={
    "price": 2.29,
    "description": "The classic retractable gel pen.",
    "quantity": 150,
    "target_quantity": 100,
    "brand": brand_pilot,
    "category": cat_pen,
    "color": "Black",
    "tip_size": 0.7
  }
)

Pen.objects.get_or_create(
  name="Uni-ball Signo DX",
  defaults={
    "price": 2.49,
    "description": "Ultra-fine gel pen with archival-quality ink.",
    "quantity": 80,
    "target_quantity": 50,
    "brand": brand_uniball,
    "category": cat_pen,
    "color": "Blue",
    "tip_size": 0.38
  }
)

Pen.objects.get_or_create(
  name="Zebra Sarasa Clip",
  defaults={
    "price": 1.99,
    "description": "Vibrant gel pen with a strong binder clip.",
    "quantity": 200,
    "target_quantity": 100,
    "brand": brand_zebra,
    "category": cat_pen,
    "color": "Red",
    "tip_size": 0.5
  }
)

Pen.objects.get_or_create(
  name="Lamy Safari",
  defaults={
    "price": 29.95,
    "description": "Durable ABS plastic fountain pen, charcoal body.",
    "quantity": 40,
    "target_quantity": 20,
    "brand": brand_lamy,
    "category": cat_pen,
    "color": "Blue", # This would be the included ink cartridge
    "tip_size": 0.5  # Represents a "Fine" (F) nib
  }
)

print("--- Created Pens ---")

# --- Step 4: Create PenRefill Instances ---
PenRefill.objects.get_or_create(
  name="Pilot G2 Refill 2-Pack",
  defaults={
    "price": 4.29,
    "description": "Refill 2-pack for Pilot G2 0.7mm pens.",
    "quantity": 75,
    "target_quantity": 50,
    "brand": brand_pilot,
    "category": cat_refill,
    "color": "Black",
    "tip_size": 0.7
  }
)

PenRefill.objects.get_or_create(
  name="Uni-ball Signo DX Refill",
  defaults={
    "price": 1.80,
    "description": "Single refill for Signo DX (UMR-1).",
    "quantity": 0, # Perfect for testing your 'out_of_stock' filter
    "target_quantity": 30,
    "brand": brand_uniball,
    "category": cat_refill,
    "color": "Blue",
    "tip_size": 0.38
  }
)

PenRefill.objects.get_or_create(
  name="Lamy T10 Cartridge 5-Pack",
  defaults={
    "price": 5.50,
    "description": "Pack of 5 ink cartridges for Lamy fountain pens.",
    "quantity": 60,
    "target_quantity": 30,
    "brand": brand_lamy,
    "category": cat_refill,
    "color": "Turquoise",
    "tip_size": 0.0 # Tip size is not applicable for cartridges
  }
)

print("--- Created Pen Refills ---")
print("Sample data has been created successfully!")