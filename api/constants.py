DEFAULT_CATEGORIES = [
  {
    "name":"Pen",
    "description":"Writing instruments that use ink to create marks on paper or other surfaces.",
    "attribute_schema": ["color", "tip_size"]
  },
  {
    "name":"Pen Refill",
    "description":"Replaceable ink cartridges or inserts designed to fit specific pens.",
    "attribute_schema": ["color", "tip_size"]
  },
]

CATEGORY_CHOICES = (
  ('pen','Pen'),
  ('penrefill', 'Pen Refill')
)

STOCK_CHOICES = (
  ('in_stock', 'In Stock'),
  ('out_of_stock', 'Out of Stock'),
)

TYPE_CHOICES = [
  ('restock', 'Restock'),
  ('sale', 'Sale'),
  ('adjustment', 'Adjustment'),
]