DEFAULT_CATEGORIES = [
  {
    "name":"Pen",
    "description":"Writing instruments that use ink to create marks on paper or other surfaces.",
  },
  {
    "name":"Pen Refill",
    "description":"Replaceable ink cartridges or inserts designed to fit specific pens.",
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