from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .base import Brand, Category

class Item(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=25)
  description = models.TextField(max_length=200, blank=True, null=True)
  brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return f"{self.brand.name} {self.name}" if self.brand else self.name

class ItemVariant(models.Model):
  """
  The "Stock Keeping Unit" (SKU).
  This is the actual item you stock and sell.
  """
  
  # The "parent" item this variant belongs to
  item = models.ForeignKey(
    Item, 
    on_delete=models.CASCADE, 
    related_name='variants'
  )
  attributes = models.JSONField(
    default=dict,
    blank=True,
    help_text="Dynamic attributes based on category, e.g., {'color': 'Blue', 'tip_size': '0.7mm'}"
  )
  sku = models.CharField(max_length=100, unique=True, db_index=True, editable=False)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.IntegerField(default=0)
  target_quantity = models.PositiveIntegerField(default=0)
  
  def save(self, *args, **kwargs):
    # 1. Normalize the JSON (Sort keys alphabetically)
    if isinstance(self.attributes, dict):
      self.attributes = dict(sorted(self.attributes.items()))

    # 2. Generate the SKU string
    # Pattern: [ITEM_ID]-[ATTR1]-[ATTR2]...
    # Example: 12-BLUE-07MM
    attr_values = [slugify(str(v)).upper() for v in self.attributes.values()]
    generated_sku = f"{self.item.id}-" + "-".join(attr_values)
    
    self.sku = generated_sku
    
    super().save(*args, **kwargs)

  def __str__(self):
      return self.sku

  def add_stock(self, amount):
    """
    Helper function:
    Adds stock to this item and creates an 'inbound' transaction log
    """
    self.quantity += amount
  
  def remove_stock(self, amount):
    """
    Helper function:
    Removes stock to this item and creates an 'outbound' transaction log
    """
    if self.quantity < amount:
      raise ValueError(f"Not enough stock for {self.name}. Have {self.quantity}, need {amount}")
    
    self.quantity -= amount

  def clean(self):
    """
    This method validates the `attributes` JSON against the 
    parent `Item.Category.attribute_schema`
    """
    super().clean()
    
    if not self.item:
      # Can't validate if there's no parent Item
      return 
    
    # Get the rules from the category
    required_keys = self.item.category.attribute_schema
    
    # Get the data we have
    provided_keys = self.attributes.keys()
    
    # 1. Check for missing keys
    for key in required_keys:
      if key not in provided_keys or not self.attributes[key]:
        raise ValidationError(f"Attribute '{key}' is required for this category.")
    
    # 2. Check for extra keys
    for key in provided_keys:
      if key not in required_keys:
        raise ValidationError(f"Attribute '{key}' is not defined for this category.")