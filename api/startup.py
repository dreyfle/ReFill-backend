def create_or_get_category():
  """
  Create Categories based on the types of Items used in the System. Current Item Categories are:
  1. Pen
  2. Pen Refills
  """

  from .models import Category
  from .constants import DEFAULT_CATEGORIES

  DEFAULT_CATEGORIES = DEFAULT_CATEGORIES

  print("Checking for default categories...")

  for category_data in DEFAULT_CATEGORIES:
    category_obj, created = Category.objects.get_or_create(
      name = category_data["name"],
      defaults = {"description": category_data["description"], "attribute_schema": category_data["attribute_schema"]}
    )

    if created:
      print(f"Created category: '{category_obj.name}'")
    else:
      print(f"Category already exists: '{category_obj.name}'")

