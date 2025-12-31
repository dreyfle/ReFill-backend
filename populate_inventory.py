from django.db import transaction
from api.models import Brand, Category, Item, ItemVariant

def populate_inventory():
  try:
    with transaction.atomic():
      print("--- Starting Inventory Seed ---")
      # 1. SETUP CATEGORIES
      try:
        pen_cat = Category.objects.get(name="Pen")
        refill_cat = Category.objects.get(name="Pen Refill")
      except Category.DoesNotExist:
        print("(X) Error: Categories 'Pen' or 'Pen Refill' not found. Please run category setup first.")
        return

      # 2. SETUP BRANDS
      brands_data = [
          ("Pilot", "Popular Japanese pen manufacturer, known for G2."),
          ("Uni-ball", "Known for the Signo and Jetstream lines."),
          ("Zebra", "Japanese manufacturer, known for Sarasa and Mildliner."),
          ("Lamy", "German brand known for the Safari fountain pen."),
      ]
      brand_map = {}
      for name, desc in brands_data:
        brand, _ = Brand.objects.get_or_create(name=name, defaults={"description": desc})
        brand_map[name] = brand

      # 3. SETUP PENS (Items + Variants)
      pens_data = [
        ("Pilot G2 07", 2.29, "The classic retractable gel pen.", 150, 100, "Pilot", "Black", "0.7"),
        ("Uni-ball Signo DX", 2.49, "Ultra-fine gel pen with archival-quality ink.", 80, 50, "Uni-ball", "Blue", "0.38"),
        ("Zebra Sarasa Clip", 1.99, "Vibrant gel pen with a strong binder clip.", 200, 100, "Zebra", "Red", "0.5"),
        ("Lamy Safari", 29.95, "Durable ABS plastic fountain pen, charcoal body.", 40, 20, "Lamy", "Blue", "0.5"),
      ]

      for name, price, desc, qty, target, b_name, color, tip in pens_data:
        # Create the Base Product (Item)
        item, _ = Item.objects.get_or_create(
          name=name,
          brand=brand_map[b_name],
          category=pen_cat,
          defaults={"description": desc}
        )
        # Create the Variant (The stockable unit)
        ItemVariant.objects.get_or_create(
          item=item,
          attributes={"color": color, "tip_size": tip},
          defaults={
              "price": price,
              "quantity": qty,
              "target_quantity": target
          }
        )

      # 4. SETUP REFILLS (Items + Variants)
      refills_data = [
          ("Pilot G2 Refill 2-Pack", 4.29, "Refill 2-pack for Pilot G2 0.7mm pens.", 75, 50, "Pilot", "Black", "0.7"),
          ("Uni-ball Signo DX Refill", 1.80, "Single refill for Signo DX (UMR-1).", 0, 30, "Uni-ball", "Blue", "0.38"),
          ("Lamy T10 Cartridge", 5.50, "Pack of 5 ink cartridges for Lamy fountain pens.", 60, 30, "Lamy", "Turquoise", "0"),
      ]

      for name, price, desc, qty, target, b_name, color, tip in refills_data:
          item, _ = Item.objects.get_or_create(
              name=name,
              brand=brand_map[b_name],
              category=refill_cat,
              defaults={"description": desc}
          )
          ItemVariant.objects.get_or_create(
              item=item,
              attributes={"color": color, "tip_size": tip},
              defaults={
                  "price": price,
                  "quantity": qty,
                  "target_quantity": target
              }
          )

      print("--- Inventory Seeded Successfully! ---")
      print(f"Created {ItemVariant.objects.count()} total stock variants.")

  except Exception as e:
    print(f"(X) Error during seed: {e}")

populate_inventory()