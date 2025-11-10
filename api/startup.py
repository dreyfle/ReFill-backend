def create_or_get_category():
  """
  Create Categories based on the types of Items used in the System. Current Item Categories are:
  1. Pen
  2. Pen Refills
  """

  from .models import Category

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

  print("Checking for default categories...")

  for category_data in DEFAULT_CATEGORIES:
    category_obj, created = Category.objects.get_or_create(
      name = category_data["name"],
      defaults = {"description": category_data["description"]}
    )

    if created:
      print(f"Created category: '{category_obj.name}'")
    else:
      print(f"Category already exists: '{category_obj.name}'")

